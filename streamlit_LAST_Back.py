import re
import requests
import random


def get_album_tags(artist_name, album_title, api_key):
   
    strings_to_remove = ["fav", " I ", artist_name,album_title,'best','die','Fav','Die','Best','10s','00s','90s','seen']
    
    strings_to_remove = [item.lower() for item in strings_to_remove]
 
   
    base_url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        'method': 'album.getTopTags',
        'artist': artist_name,
        'album': album_title,
        'api_key': api_key,
        'format': 'json'
    }

    response = requests.get(base_url, params=params)
    
    
    tag_list = [d['name'] for d in response.json()['toptags']['tag']]
    
    tag_list = [item.lower() for item in tag_list]
    
    filtered_list = [item for item in tag_list if not any(string in item for string in strings_to_remove)]

    filtered_list = [item for item in filtered_list if not re.match(r'^\d+$', item)]

    
    return filtered_list



def get_album_info(artist_name, album_title, api_key):
   

   
    base_url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        'method': 'album.getInfo',
        'artist': artist_name,
        'album': album_title,
        'api_key': api_key,
        'format': 'json'
    }

    response = requests.get(base_url, params=params)
    
    
    
    return response.json()



def album_with_tag(tag, limit, page):
   
   
   
    base_url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        'method': 'tag.getTopAlbums',
        'tag': tag,
        'limit': limit,
        'page': page,
        'api_key': api_key,
        'format': 'json'
    }

    response = requests.get(base_url, params=params)
    
    return response.json()


a1 = "NewJeans"
al1 = "NewJeans 'Super Shy'"
a2 = 'BTS'
al2 = 'The Most Beautiful Moment in Life: Young Forever'

# Example usage
api_key = '5b06c4e904f307e09b5f7c3155d30212'  # Replace with your actual API key


# Fetch album tags
tag_list_1 = get_album_tags(a1, al1, api_key)
tag_list_2 = get_album_tags(a2, al2, api_key)

album1 = get_album_info(a1, al1, api_key)
album2 = get_album_info(a2, al2, api_key)


#common_elements 

common_elements = list(set(tag_list_1[0:40]).intersection(tag_list_2[0:40]))

limit=200
page=1

try:
    tag = common_elements[0]
except:
    tag=tag_list_1[0]


albums_with_tag_name = album_with_tag(tag,limit,page)

matching_albums = []

for i in range(len(albums_with_tag_name['albums']['album'])):
    
    artist = albums_with_tag_name['albums']['album'][i]['artist']['name']
        
    album_name = albums_with_tag_name['albums']['album'][i]['name']
    
    tag_list_rec = get_album_tags(artist, album_name, api_key)
    
    # Calculate the common elements between tag_list_rec and tag_list_1
    common_elements_1 = list(set(tag_list_rec[0:60]).intersection(tag_list_1[0:60]))
    
    # Calculate the common elements between tag_list_rec and tag_list_2
    common_elements_2 = list(set(tag_list_rec[0:60]).intersection(tag_list_2[0:60]))

    
    # Check if both common_elements_1 and common_elements_2 have more than 3 common elements
    if len(common_elements_1) >= 2 and len(common_elements_2) >= 2:
        # Create a dictionary for the matching album
        matching_album = {
            'album_name': album_name,
            'artist': artist,
            'common_elements_1': common_elements_1,
            'common_elements_2': common_elements_2
        }
        # Append the matching album dictionary to the list
        matching_albums.append(matching_album)
        


while True:
    
    random_album = random.choice(matching_albums)
    
    rec_album_info = get_album_info(random_album['artist'], random_album['album_name'],api_key)

    rec_listeners = rec_album_info['album']['listeners']
    
    try:

        rec_length = len(rec_album_info['album']['tracks']['track'])
        
    except:
        
        rec_length = 0
    
    if int(rec_listeners) < 1000000 and int(rec_length) > 7:
        
        common_1 = random_album['common_elements_1']
        common_2 = random_album['common_elements_2']
    
        break



   
    






