import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_lottie import st_lottie


st.set_page_config(page_title='Movie Recommender',page_icon=':🎬:')


# pickling .pkl files
movies_dict = pickle.load(open('models/movies_dict.pkl','rb'))
similarity = pickle.load(open('models/Movies_similarity.pkl','rb'))

# pandas dataframe was unable to pickle directly in read mode, so first converted to dictonary in jupyter notebook and then pickled here
movies = pd.DataFrame(movies_dict)



###########################################################################################################


#CREATING A FETCH_POSTER FUNCTION TO FETCH POSTER BASED ON MOVIE_ID FROM URL
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=47f5dabb1b608b91fe3ef3ad90ffef57&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# CREATING A RECOMMEND FUNCTION FOR TOP5 SIMILAR MOVIES
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

def display_typed_movie(movie):
    movie_index = movies[ movies['title'] == movie].index[0]
    movie_id = movies.iloc[movie_index].movie_id
    typed_movie_poster = fetch_poster(movie_id)
    typed_movie_title = movies.title[movie_index]
    return typed_movie_title , typed_movie_poster



##########################################################################################################


# https://lottiefiles.com/

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    else:
        return r.json()

lottie_coding = load_lottieurl('https://lottie.host/fa421b97-2ad5-4963-b33a-cb1d8ce5a9d1/BybCb1QyHz.json')
st_lottie(lottie_coding,height=200)


# creating Title to display on server
# https://www.webfx.com/tools/emoji-cheat-sheet/
st.title('Movie Recommender 🎭')


# creating recommend button
selected_movie_name = st.selectbox(
    'Type or select a movie from the dropdown',
    movies['title'].values
)
if st.button('Recommend'):
    typed_movie_name,typed_movie_poster = display_typed_movie(selected_movie_name)
    st.write("---")
    col0, _, _ = st.columns([1, 1, 1])
    with col0:
        st.text(typed_movie_name)
        st.image(typed_movie_poster)
    st.write("---")

    st.subheader('Top 5 recommendations for ' + typed_movie_name +' are :')
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])






