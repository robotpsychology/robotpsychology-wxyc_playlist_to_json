import os
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

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

def wxyc_playlist_parser(url, playlist_name=f"wxyc_live_playlist {datetime.now().strftime('%m-%d-%Y_%H-%M-%S-%p')}"):
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
    music_dict = {}

    for rows in tr:
        parsed_content.append(rows.contents)

    for lst in parsed_content:
        for item in lst:
            if item == '\n':
                lst.remove(item)
        
        dict_formatted_content.append([item.string for item in lst])
    
    # print(parsed_content)
    # print(dict_formatted_content)

    counter = 0
    for lst in dict_formatted_content:
        music_dict[counter] = {
            'request': None,
            'artists': None,
            'song': None,
            'album': None,
            'label': None
        }
        if lst[0] == '*':
            music_dict[counter]['request'] = True
        else:
            music_dict[counter]['request'] = False

        music_dict[counter]['artists'] = lst[1]
        music_dict[counter]['song'] = lst[2]
        music_dict[counter]['album'] = lst[3]
        music_dict[counter]['label'] = lst[4]

        counter += 1


    # Make sure to look at first run file to see an error we need to catch. The use of odd symbols such as A with tilde and copyright symbol.
    with open(clean_file_name(f"{playlist_name}") + '.json', "w") as outfile:
        json.dump(music_dict, outfile, indent=4)

    return music_dict


    
# Live Playlist example:
wxyc_playlist_parser('http://www.wxyc.info/playlists/recent.html')

# Archived Playlist: 
wxyc_playlist_parser('http://wxyc.info/playlists/radioShow?radioShowID=156207', 'DJ Appa 7/18/21 3AM-6AM')






