import streamlit as st
import os, sys

@st.cache_resource
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()

import requests
import random
from streamlit_LAST_Back import get_album_tags, get_album_info, album_with_tag

# Define the titles
# Define the titles
title = (f"<div style='text-align: center; font-size: 66px; color: #F5F5F5; font-weight: bold;'>SoundSurfer</div>")
sub_title = (f"<div style='text-align: center; font-size: 26px; color: #F5F5F5;'>Enter two albums and get a new recommendation!</div>")

# Create a two-column layout
col1, col2 = st.columns([3, 1])  # Adjust the width ratios as needed (1:2 in this example)

# Add the title and subtitle to the first column
col1.markdown(title, unsafe_allow_html=True)

# Add a smaller-sized image to the second column
image_path = "SoundSurfer.png"  # Replace with the actual path to your PNG image
col2.image(
    image_path,
    use_column_width=False,  # Disable column width adaptation
    width=130,  # Adjust the image width as needed
)

# Add CSS to adjust the padding
st.markdown(
    "<style>"
    ".stImage { padding-left: 80px; }"  # Adjust the left padding as needed
    "</style>",
    unsafe_allow_html=True
)

st.write('')
st.markdown(sub_title, unsafe_allow_html=True)
st.write('')




a1 = (st.text_input('Artist 1')).lower()
al1 = (st.text_input('Album 1')).lower()
a2 = (st.text_input('Artist 2')).lower()
al2 = (st.text_input('Album 2')).lower()

progress_bar = st.progress(0)

# Assuming you have different stages in your app, update the progress bar accordingly
 
# Custom styled button with central alignment using HTML and CSS
button_style = """
    <style>
        /* Container for the button to help in centering */
        div.stButton {
            display: flex;
            justify-content: center;
        }

        /* Style for the native Streamlit button */
        div.stButton > button:first-child {
            background-color: #f8f8f8;  /* Off-white background */
            color: black;               /* Black text */
            border: 1px solid black;    /* Black border */
            border-radius: 4px;         /* Rounded corners */
            padding: 10px 20px;         /* Bigger size */
        }
    </style>
"""

st.markdown(button_style, unsafe_allow_html=True)


if 'current_message' not in st.session_state:
    st.session_state.current_message = ''

# Listen for custom button events
if st.button('Reccomend!'):
    
    
    text = st.empty()
    
    st.write('')
    text.write("Checking Albums...", value="", key="1")
    
    # Example usage
    api_key = '5b06c4e904f307e09b5f7c3155d30212'  # Replace with your actual API key
    
    
    # Fetch album tags
    tag_list_1 = get_album_tags(a1, al1, api_key)
    tag_list_2 = get_album_tags(a2, al2, api_key)
    
    album1 = get_album_info(a1, al1, api_key)
    album2 = get_album_info(a2, al2, api_key)
    
    album1_image = album1['album']['image'][5]['#text']
    
    album2_image = album2['album']['image'][5]['#text']
    
    #col1, col2 = st.columns([3, 1])  # Adjust the width ratios as needed (1:2 in this example)

    # Add the title and subtitle to the first column
    #col1.image(
      #  album1_image,
     #   use_column_width=False,  # Disable column width adaptation
     #   width=200,)  # Adjust the image width as needed
    # Add a smaller-sized image to the second column
    #col2.image(
     #   album2_image,
     #   use_column_width=False,  # Disable column width adaptation
     #   width=200,  # Adjust the image width as needed
   # )

    
    
    #common_elements 
    
    common_elements = list(set(tag_list_1[0:40]).intersection(tag_list_2[0:40]))
    
    limit=250
    page=1
    
    try:
        tag = common_elements[0]
    except:
        tag=tag_list_1[0]
    
    
    albums_with_tag_name = album_with_tag(tag,limit,page)

    
    progress_bar.progress(20)
    
    matching_albums = []
    
    
    text.write("Finding Similar Albums...", value="", key="2")

    
    for i in range(len(albums_with_tag_name['albums']['album'])):
        
        artist = albums_with_tag_name['albums']['album'][i]['artist']['name']
            
        album_name = albums_with_tag_name['albums']['album'][i]['name']
        
        tag_list_rec = get_album_tags(artist, album_name, api_key)
        
        # Calculate the common elements between tag_list_rec and tag_list_1
        common_elements_1 = list(set(tag_list_rec[0:60]).intersection(tag_list_1[0:60]))
        
        # Calculate the common elements between tag_list_rec and tag_list_2
        common_elements_2 = list(set(tag_list_rec[0:60]).intersection(tag_list_2[0:60]))
    
        
        # Check if both common_elements_1 and common_elements_2 have more than 3 common elements
        if len(common_elements_1) >= 3 and len(common_elements_2) >= 3:
            # Create a dictionary for the matching album
            matching_album = {
                'album_name': album_name,
                'artist': artist,
                'common_elements_1': common_elements_1,
                'common_elements_2': common_elements_2
            }
            # Append the matching album dictionary to the list
            matching_albums.append(matching_album)
            
    
    progress_bar.progress(40)
    
    #st.write(matching_albums)
    
    
    text.write("Matching Albums...", value="", key="3")
    
    while True:
        
        random_album = random.choice(matching_albums)
        
        rec_album_info = get_album_info(random_album['artist'], random_album['album_name'],api_key)
    
        rec_listeners = rec_album_info['album']['listeners']
        
        try:
    
            rec_length = len(rec_album_info['album']['tracks']['track'])
            
        except:
            
            rec_length = 0
        
        if int(rec_listeners) < 500000 and int(rec_length) > 7:
            
            FINAL_ALBUM = rec_album_info['album']['name']
            FINAL_ARTIST = rec_album_info['album']['artist']
            
            common_1 = random_album['common_elements_1']
            common_2 = random_album['common_elements_2']
        
            break
    
    
    
    rec_image = rec_album_info['album']['image'][5]['#text']
    
    #st.image(rec_image, use_column_width=False, width=130,)

    
    
    progress_bar.progress(80)
    
   
    text.write("", value="", key="4")
    
    st.write('')
    recommendation_text = f"<div style='text-align: center; font-size: 30px;'>Your Recommendation is:</div>"
    recommendation_text_2 = f"<div style='text-align: center; font-size: 32px;'><strong>{FINAL_ALBUM}</strong> by <em>{FINAL_ARTIST}</em>.</div>"
    
    
    st.markdown(recommendation_text, unsafe_allow_html=True)
    st.markdown(recommendation_text_2, unsafe_allow_html=True)
    st.write('')


    import matplotlib.pyplot as plt

    # Assuming common_genres_1, common_genres_2, common_descriptors_1, and common_descriptors_2 are your lists
    # Calculate the number of common elements for each album

    
    # Labels for the pie chart
    labels = [al1.title(), al2.title()]
    
    # Values for each section of the pie chart
    sizes = [len(common_1), len(common_2)]
    
    # Colors for each section
    colors = ['#ece8d9','#8cb0c5']
    
    # Plotting the pie chart
    fig1, ax1 = plt.subplots()
    _, texts, _ = ax1.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'color': 'black'})
    
    # Set the text color for each label individually
    texts[0].set_color(colors[0])   # Set the text color for the first label to red
    texts[1].set_color(colors[1])  # Set the text color for the second label to blue
    
    
    

    
    # Draw circle for a Donut chart

    # Equal aspect ratio ensures that pie is drawn as a circle
    
    plt.tight_layout()
    fig1.patch.set_facecolor('none') # Set figure background to transparent
    fig1.patch.set_alpha(0) # Set transparency level
    ax1.patch.set_facecolor('none') # Set axes background to transparent
    
    st.write('')
    pie_title = f"<h3 style='font-size: 38px; text-align: center;'>Album Similarity</h3>"

    st.markdown(pie_title, unsafe_allow_html=True)
    st.write(
        '<style>div.Widget.row-widget.stRadio {justify-content: center;}' 
        'div.row-widget.stRadio div {margin-left: 50px;}</style>',
        unsafe_allow_html=True
        )

    # Show the plot
    st.pyplot(fig1)
    
    
    color_genre_1 = "#ece8d9"
    color_descriptor_1 = "#f7f5ee"  
    
    color_genre_2 = "#8cb0c5"
    color_descriptor_2 = "#c2d5e0"  

    
    html_content_1 = "<ul>"

    # Add all genres
    for tag in common_1:
        html_content_1 += f"<li style='color: {color_descriptor_1};'><b>{tag.title()}</b></li>"

    # Close the unordered list
    html_content_1 += "</ul>"
    
    
    html_content_2 = "<ul>"

    # Add all genres
    for tag in common_2:
        html_content_2 += f"<li style='color: {color_descriptor_2};'><b>{tag.title()}</b></li>"

    # Close the unordered list
    html_content_2 += "</ul>"
    
    col1, col2 = st.columns(2)
    
    with col1:
        markdown_text = f"<h3 style='font-size: 24px; text-align: center; color: color_genre_1;'>{al1.title()}</h3>"
        st.markdown(markdown_text, unsafe_allow_html=True)
        st.markdown(html_content_1, unsafe_allow_html=True)
    
    with col2:
        markdown_text = f"<h3 style='font-size: 24px; text-align: center; color: color_genre_2;'>{al2.title()}</h3>"

        st.markdown(markdown_text, unsafe_allow_html=True)
        st.markdown(html_content_2, unsafe_allow_html=True)

    
    progress_bar.progress(100)

    
