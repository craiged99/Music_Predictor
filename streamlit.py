import streamlit as st
import os, sys

@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()

import requests
import random
from selenium import webdriver
from selenium.webdriver import FirefoxOptions


opts = FirefoxOptions()
opts.add_argument("--headless")

st.markdown('MUSIC PREDICTOR')

a1 = st.text_input('Artist 1')
al1 = st.text_input('Album 1')
a2 = st.text_input('Artist 2')
al2 = st.text_input('Album 2')

if a1 and al1 and a2 and al2:
    artist = a1.replace(' ','-')
    album = al1.replace(' ','-')
    artist2 = a2.replace(' ','-')
    album2 = al2.replace(' ','-')
        
    st.write('')
    st.write('Checking Albums...')
    driver = webdriver.Firefox(options=opts)
    driver.get("https://rateyourmusic.com/release/album/"+artist+"/"+album+'/')
    driver2 = webdriver.Firefox(options=opts)
    driver2.get("https://rateyourmusic.com/release/album/"+artist2+"/"+album2+'/')


    st.write('')
    st.write('Getting Album Information...')
    html = driver.page_source
    descriptors_1 = (html.split('release_pri_descriptors">')[1]).split('</span')[0].split(',  ')
    html = html.split()

    html2 = driver2.page_source
    descriptors_2 = (html2.split('release_pri_descriptors">')[1]).split('</span')[0].split(',  ')
    html2 = html2.split()

    list1 = [ x for x in html if "genre/" in x ]
    new_list = [s.replace('href="/genre/', "") for s in list1]
    genres_1 = [s.split('/', 1)[0] for s in new_list]

    genres_1 = [item for item in genres_1 if '=' not in item]

    list12 = [ x for x in html2 if "genre/" in x ]
    new_list2 = [s.replace('href="/genre/', "") for s in list12]
    genres_2 = [s.split('/', 1)[0] for s in new_list2]

    genres_2 = [item for item in genres_2 if '=' not in item]

    #Look for common genres/descript. between albums
    common_genres = [element for element in genres_1 if element in genres_2]
    common_descriptors = [element for element in descriptors_2 if element in descriptors_1]


    random_number = random.randint(1, 2)

    try:
        final_genres  = random.sample(common_genres, 1)

        genre_version = 1  
        
    except:
        if random_number == 1:
            final_genres  = random.sample(genres_1, 1)
            
        else:
            final_genres  = random.sample(genres_2, 1)

        genre_version = 2
        
   
            
    if random_number == 1:
        
        try: 
            
            final_desciptors  = random.sample(descriptors_2,2)
            
        except:
            final_desciptors = random.sample(descriptors_2+descriptors_2,2)

    else:
        try: 
            
            final_desciptors  = random.sample(descriptors_1,2)
            
        except:
            final_desciptors = random.sample(descriptors_2+descriptors_2,2)



    final_genres = [s.replace('-', " ") for s in final_genres]
    final_genres = [s.split(' ') for s in final_genres]

    final_desciptors = [s.replace('-', " ") for s in final_desciptors]
    final_desciptors = [s.split(' ') for s in final_desciptors]


    url = 'https://rateyourmusic.com/charts/diverse/album/all-time/ge:exact,'

    for i in range(len(final_genres)):
        for j in range(len(final_genres[i])):
            genre_words = len(final_genres[i])
            if j == genre_words-1:
                url = url + final_genres[i][j] + ','
            else:
                url = url + final_genres[i][j] + '%2d'
                
    url = url + '/d:all,'
                
    for i in range(len(final_desciptors)):
        for j in range(len(final_desciptors[i])):
            genre_words = len(final_desciptors[i])
            if j == genre_words-1:
                url = url + final_desciptors[i][j] + ','
            else:
                url = url + final_desciptors[i][j] + '%2d'
                



    st.write('')
    st.write('Predicting New Album...')
    driver = webdriver.Firefox(options=opts)
    driver.get(url)
    html_genre = driver.page_source
    html_genre = html_genre.split()

    list3 = [ x for x in html_genre if 'release/album/' in x ]
    list3 = list(set(list3))
    albums = list(dict.fromkeys(list3))
    no_shite = [s.replace('href="/release/album/', "") for s in albums]
    no_shite = [s.replace('/">', "") for s in no_shite]

    filtered_list = [item for item in no_shite if artist not in item]
    filtered_list = [item for item in filtered_list if artist2 not in item]

    try:
        random_no = random.randrange(1, len(filtered_list), 1)
        
    except:
        url = 'https://rateyourmusic.com/charts/diverse/album/all-time/ge:exact,'

        for i in range(len(final_genres)):
            for j in range(len(final_genres[i])):
                genre_words = len(final_genres[i])
                if j == genre_words-1:
                    url = url + final_genres[i][j] + ','
                else:
                    url = url + final_genres[i][j] + '%2d'
                    
        url = url + '/d:'
                    
        for i in range(len(final_desciptors)):
            for j in range(len(final_desciptors[i])):
                genre_words = len(final_desciptors[i])
                if j == genre_words-1:
                    url = url + final_desciptors[i][j] + ','
                else:
                    url = url + final_desciptors[i][j] + '%2d'
                    

       

        st.write('')
        st.write('Predicting New Album...')
        driver = webdriver.Firefox(options=opts)
        driver.get(url)
        html_genre = driver.page_source
        html_genre = html_genre.split()

        list3 = [ x for x in html_genre if 'release/album/' in x ]
        list3 = list(set(list3))
        albums = list(dict.fromkeys(list3))
        no_shite = [s.replace('href="/release/album/', "") for s in albums]
        no_shite = [s.replace('/">', "") for s in no_shite]

        filtered_list = [item for item in no_shite if artist not in item]
        filtered_list = [item for item in filtered_list if artist2 not in item]
        
        random_no = random.randrange(1, len(filtered_list), 1)
        

    reccomendation = filtered_list[random_no]
    rec_artist = reccomendation.split('/',1)[0]
    rec_artist_space = rec_artist.replace('-',' ')
    rec_album = reccomendation.split('/',1)[1]
    rec_album_space = rec_album.replace('-',' ')


    driver_recommend = webdriver.Firefox(options=opts)
    driver_recommend.get("https://rateyourmusic.com/release/album/"+rec_artist+"/"+rec_album+'/')


    html_recommend = driver_recommend.page_source
    descriptors_reccomend = (html_recommend.split('release_pri_descriptors">')[1]).split('</span')[0].split(',  ')
    html_recommend = html_recommend.split()

    list_reccomend = [ x for x in html_recommend if "genre/" in x ]
    list_reccomend = [s.replace('href="/genre/', "") for s in list_reccomend]
    list_reccomend = [s.split('/', 1)[0] for s in list_reccomend]


    st.write('')
    st.write('Getting New Album Information...')

    common_genres_1 = [element for element in list_reccomend if element in genres_1]
    common_descriptors_1 = [element for element in descriptors_reccomend if element in descriptors_1]



    common_genres_2 = [element for element in list_reccomend if element in genres_2]
    common_descriptors_2 = [element for element in descriptors_reccomend if element in descriptors_2]

    common_descriptors_both = [element for element in descriptors_reccomend if element in common_descriptors]
    common_genres_both = [element for element in list_reccomend if element in common_genres]


    common_genres_1 = list(set(common_genres_1))
    common_genres_2 = list(set(common_genres_2))

    Reccomend = 'I reccomend ' + rec_album_space+' by '+rec_artist_space + '.'


    #genre_recoomned
    if len(common_genres_both) != 0:
        
        genre_string = 'This album has genres of ' + ' and '.join(common_genres_both) + ' that are also present in both original albums.'

    if len(common_genres_both) == 0 and len(common_genres_1) != 0 and len(common_genres_2) !=0:
        
        genre_string = 'This album is ' + common_genres_1[0] +', similar to ' + album +\
            ', whilst also having elements of ' + common_genres_2[0] + ', like ' + album2 + '.'
            
    else:
        if random_number == 1:
            genre_string = 'This album has genres of ' + ' and '.join(common_genres_1) +\
                ' that are also present in ' +album + '.'
                
        if random_number == 2:
            genre_string = 'This album has genres of ' + ' and '.join(common_genres_2)+\
                ' that are also present in ' +album2 + '.'



    descript_string = ''

    #descriptors
    if len(common_descriptors_both) != 0:
        
        if len(common_descriptors_both) == 1:
            
            if random_number == 1:
        
                descript_string = 'Similar to both original albums, this suggested album is described as ' + \
                    common_descriptors_both[0] + ', whilst also being described as ' + \
                        common_descriptors_2[0] + ', similar to ' + album2 + '.'
                        
            if random_number == 2:
        
                descript_string = 'Similar to both original albums, this suggested album is described as ' + \
                    common_descriptors_both[0] + ', whilst also being described as ' + \
                        common_descriptors_1[0] + ', similar to ' + album + '.'
                        
        if len(common_descriptors_both) >= 2:
            
            descript_string = 'Similar to both original albums, this suggested album is described as ' + \
                ' and '.join(common_descriptors_both[0:2]) + '.'
                
    if len(common_descriptors_both) == 0:
        
        if random_number == 1:

            descript_string = 'Similar to ' + album2 + ', this suggested album is described as ' + \
                ' and '.join(common_descriptors_2[0:2]) + '.'
                    
        if random_number == 2:

            descript_string = 'Similar to ' + album + ', this suggested album is described as ' + \
                ' and '.join(common_descriptors_1[0:2]) + '.'
                
          
    Reccomend = Reccomend + ' ' + genre_string + ' ' + descript_string
    Reccomend = Reccomend.replace('-',' ')

    st.write('')
    st.write(Reccomend)
    st.write(' ')
