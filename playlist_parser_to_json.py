import os
import requests
from bs4 import BeautifulSoup
import json

def wxyc_playlist_parser():
    html_doc = requests.get('http://www.wxyc.info/playlists/recent.html')
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    # print(html_doc.text)
    # print(html_doc.encoding)

    # print(soup.title)

    tr = soup.find_all('tr', attrs={'bgcolor': '#F3F3F3'})

    data_list = []
    new_data_list = []
    music_dict = {}

    # data_list = {
    #     'empty_cell': {},
    #     'request': {},
    #     'song_info': {
    #             {'artist':, 'song':, 'album':, 'label': }
    #         }
    #     'empty_cell_2': {}
    # }

    
    for rows in tr:
        data_list.append(rows.contents)

    for lst in data_list:
        for item in lst:
            if item == '\n':
                lst.remove(item)
        
        new_data_list.append([item.string for item in lst])
    
    print(data_list)

    print(new_data_list)

    counter = 0
    for lst in new_data_list:
        counter += 1
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



    print(music_dict)

    json_object = json.dumps(music_dict, indent = 4)
    print(json_object)

    with open("live_playlist.json", "w") as outfile:
        json.dump(music_dict, outfile, indent=4)




            


wxyc_playlist_parser()



