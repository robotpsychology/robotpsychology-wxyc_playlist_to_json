import os
import requests
import json
from bs4 import BeautifulSoup

def wxyc_playlist_parser(url):
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
    with open("live_playlist.json", "w") as outfile:
        json.dump(music_dict, outfile, indent=4)

    return music_dict


    




            


wxyc_playlist_parser('http://www.wxyc.info/playlists/recent.html')



