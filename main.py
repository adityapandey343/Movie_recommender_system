import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f88587970794a746223989bac082a0df&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/original' + data['poster_path']


movies_dict = pickle.load(open('movie_dict.pkl', "rb"))
similarity = pickle.load(open('similarity.pkl', "rb"))


movies = pd.DataFrame(movies_dict)


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=(lambda x: x[1]))[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_poster


Title = f'<B><p style="font-family:Lucida Handwriting; color:White; font-size: 40px;">Movie Recommendor System</p></B>'
st.markdown(Title, unsafe_allow_html=True )

selcted_movie_name = st.selectbox(

    '',
    movies['title'].values)

if st.button("Recommend"):
    names,posters = recommend(selcted_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        new_title = f'<p style="font-family:sans-serif; color:White; font-size: 15px;">{names[0]}</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.image(posters[0])
    with col2:
        new_title = f'<p style="font-family:sans-serif; color:White; font-size: 15px;">{names[1]}</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.image(posters[1])
    with col3:
        new_title = f'<p style="font-family:sans-serif; color:White; font-size: 15px;">{names[2]}</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.image(posters[2])
    with col4:
        new_title = f'<p style="font-family:sans-serif; color:White; font-size: 15px;">{names[3]}</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.image(posters[3])
    with col5:
        new_title = f'<p style="font-family:sans-serif; color:White; font-size: 15px;">{names[4]}</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.image(posters[4])

import base64


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )


add_bg_from_local('Untitled.png')
