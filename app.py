import pickle
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load the API key
load_dotenv()  # only affects local runs
OMDB_API_KEY = (
    os.getenv("OMDB_API_KEY")
    or st.secrets.get("OMDB_API_KEY")
)
def fetch_poster(movie_id):
    url = f"http://www.omdbapi.com/?i={movie_id}&apikey={OMDB_API_KEY}"
    data = requests.get(url).json()
    poster_path = data.get('Poster')

    # return placeholder if poster is missing
    if not poster_path or poster_path == "N/A":
        return "https://via.placeholder.com/300x450?text=No+Poster"
    return poster_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['movieId']
        imdb_id = movieId_to_imdb.loc[movieId_to_imdb['movieId'] == movie_id, 'imdb_id_formatted'].values[0]
        recommended_movie_posters.append(fetch_poster(imdb_id))
        recommended_movie_names.append(movies.iloc[i[0]]['title'])
    return recommended_movie_names, recommended_movie_posters

st.header('🎬 Movie Recommender System')

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movieId_to_imdb = pickle.load(open('movieId_to_imdb.pkl', 'rb'))


movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
