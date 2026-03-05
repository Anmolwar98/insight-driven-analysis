import streamlit as st
import pickle
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Page config
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Load data
@st.cache_data
def load_data():
    movies_df = pickle.load(open(os.path.join(BASE_DIR, "movies.pkl"), "rb"))
    similarity = pickle.load(open(os.path.join(BASE_DIR, "similarity.pkl"), "rb"))
    return movies_df, similarity

movies_df, similarity = load_data()


# Function to fetch full poster URL
def fetch_poster(poster_path):
    if pd.notna(poster_path) and poster_path != "":
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None


# Recommendation function
def recommend(movie):
    recommended_movies = []

    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_lst = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    for i in movies_lst:
        movie_data = movies_df.iloc[i[0]]

        recommended_movies.append({
            "title": movie_data.title,
            "poster": fetch_poster(movie_data.poster_path)
        })

    return recommended_movies


# UI
st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Find movies similar to your favorite one</p>", unsafe_allow_html=True)

st.divider()

selected_movie_name = st.selectbox(
    "Select a Movie",
    movies_df['title'].values
)

if st.button("🔍 Recommend Movies"):

    recommendations = recommend(selected_movie_name)

    st.subheader("Top Recommendations")

    cols = st.columns(5)

    for idx, movie in enumerate(recommendations):

        with cols[idx]:

            st.markdown(f"**{movie['title']}**")

            if movie["poster"]:
                st.image(movie["poster"], use_container_width=True)
            else:
                st.write("Poster not available")