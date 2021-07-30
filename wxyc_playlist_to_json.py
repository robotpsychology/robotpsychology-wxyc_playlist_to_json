import os
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

# THE LIVE PLAYLSIST PAGE AND ARCHIVE PAGES ARE FORMATTED DIFFERENTLY. CREATE A FUNCTION FOR EACH, THEN A MAIN FUNCTION THAT DETERMINES WHICH TYPE OF PAGE IT IS AND RUNS THE APPROPRIATE FUNCTION.

def clean_file_name(sourcestring,  removestring="%:/,.\\[]<>*?"):
    """Taken and slightly modified from https://www.programcreek.com/python/?CodeExample=clean+filename"""
    
    """Clean a string by removing selected characters.

    Creates a legal and 'clean' source string from a string by removing some 
    clutter and  characters not allowed in filenames.
    A default set is given but the user can override the default string.

    Args:
        | sourcestring (string): the string to be cleaned.
        | removestring (string): remove all these characters from the string (optional).

    Returns:
        | (string): A cleaned-up string.

    Raises:
        | No exception is raised.
    """
    #remove the undesireable characters
    return ''.join([c for c in sourcestring if c not in removestring])



def playlist_url_parser(url, playlist_name):
    """
    Argument 1: WXYC Playlist URL
    Argument 2 (optional): Input desired JSON filename if you are parsing a playlist that is not the current live playlist. 
        Will automatically include current date and time. If custom name is inputted, it will be cleaned of potential forbidden file characters.
    """
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    tr = soup.find_all('tr', attrs={'bgcolor': '#F3F3F3'})

    parsed_content = []
    dict_formatted_content = []

    for rows in tr:
        parsed_content.append(rows.contents)

    for lst in parsed_content:
        for item in lst:
            if item == '\n':
                lst.remove(item)
        
        dict_formatted_content.append([item.string for item in lst])
    
    # print(parsed_content[1], parsed_content[18])
    # print(dict_formatted_content)


    if '/playlists/recent.html' in url:
        return dict_formatted_content, 'live'
    elif 'playlists/radioShow?radioShowID' in url:
        return dict_formatted_content, 'archive'
    # elif 'playlists/searchPlaylists' in url:
    #     return dict_formatted_content, 'search' 
    else:
        print('Invalid URL')
        return None



def wxyc_live_playlist_dict(dict_formatted_content):
    counter = 0
    music_dict = {}

    for lst in dict_formatted_content:
        music_dict[counter] = {
            'rotation': None,
            'artist': None,
            'song': None,
            'release': None,
            'label': None,
            'request': None,
        }

        if lst[0] == '*':
            music_dict[counter]['rotation'] = True
        else:
            music_dict[counter]['rotation'] = False

        if lst[-1] == '*':
            music_dict[counter]['request'] = True
        else:
            music_dict[counter]['request'] = False

        music_dict[counter]['artist'] = lst[1]
        music_dict[counter]['song'] = lst[2]
        music_dict[counter]['release'] = lst[3]
        music_dict[counter]['label'] = lst[4]

        counter += 1

    return music_dict


def wxyc_archive_playlist_dict(dict_formatted_content):
    counter = 0
    music_dict = {}

    for lst in dict_formatted_content:
        music_dict[counter] = {
            'rotation': None,
            'request': None,
            'artist': None,
            'song': None,
            'release': None,
            'label': None
        }

        if lst[0] == '*':
            music_dict[counter]['rotation'] = True
        else:
            music_dict[counter]['rotation'] = False

        if lst[1] == '*':
            music_dict[counter]['request'] = True
        else:
            music_dict[counter]['request'] = False

        music_dict[counter]['artist'] = lst[1]
        music_dict[counter]['song'] = lst[2]
        music_dict[counter]['release'] = lst[3]
        music_dict[counter]['label'] = lst[4]

        counter += 1

    return music_dict


# def wxyc_search_playlist_dict(dict_formatted_content):
    counter = 0
    music_dict = {}

    for lst in dict_formatted_content:
        music_dict[counter] = {
            'date of show': None,
            'artist': None,
            'song': None,
            'release': None,
            'label': None
        }

        counter += 1

    return music_dict




def playlist_json_dump(music_dict, playlist_name):
    # Make sure to look at first run file to see an error we need to catch. The use of odd symbols such as A with tilde and copyright symbol.
    with open(clean_file_name(f"{playlist_name}") + '.json', "w") as outfile:
        json.dump(music_dict, outfile, indent=4)



def wxyc_playlist_to_json(url, playlist_name=f"wxyc_live_playlist {datetime.now().strftime('%m-%d-%Y_%H-%M-%S-%p')}"):
    parser_result = playlist_url_parser(url, playlist_name)
    if parser_result == None:
        print('Something went wrong. Probably a bad URL.')
        return parser_result
    
    dict_formatted_content = parser_result[0]
    playlist_type = parser_result[1]
    music_dict = {}

    if playlist_type == 'live':
        music_dict = wxyc_live_playlist_dict(dict_formatted_content)

        playlist_json_dump(music_dict, playlist_name)
    elif playlist_type == 'archive':
        music_dict = wxyc_archive_playlist_dict(dict_formatted_content)

        if 'wxyc_live_playlist' in playlist_name:
            playlist_json_dump(music_dict, f"Unnamed Archive Playlist - Downloaded {datetime.now().strftime('%m-%d-%Y')}")
        else:
            playlist_json_dump(music_dict, playlist_name)
    # elif playlist_type == 'search':
    #     music_dict = wxyc_search_playlist_dict(dict_formatted_content)

    #     if 'wxyc_live_playlist' in playlist_name:
    #         playlist_json_dump(music_dict, f"Unnamed Search Playlist - Downloaded {datetime.now().strftime('%m-%d-%Y')}")
    #     else:
    #         playlist_json_dump(music_dict, playlist_name)



    
# Live Playlist example:
wxyc_playlist_to_json('http://www.wxyc.info/playlists/recent.html')

# Archive Playlist (Forbidden Characters): 
wxyc_playlist_to_json('http://wxyc.info/playlists/radioShow?radioShowID=156207', 'DJ Appa 7/18/21 3AM-6AM')

# Archive Playlist (Left Unnamed): 
wxyc_playlist_to_json('http://wxyc.info/playlists/radioShow?radioShowID=156207')




