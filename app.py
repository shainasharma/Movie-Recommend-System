import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster based on movie ID
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=38dcc2d465228f5caeaed9da9d1b8581&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Function to recommend movies based on similarity
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # Get the index of the selected movie
    distances = similarity[movie_index]  # Get the similarity scores
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  # Sort movies by similarity, and exclude the selected movie itself

    recommended_movies = []  # List to store recommended movie titles
    recommended_movies_poster = []  # List to store recommended movie posters
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Get movie ID
        recommended_movies.append(movies.iloc[i[0]].title)  # Add movie title to the list
        recommended_movies_poster.append(fetch_poster(movie_id))  # Fetch poster and add it to the list

    return recommended_movies, recommended_movies_poster  # Return both lists

# Load data from pickle files
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))  # Load the movie dictionary
movies = pd.DataFrame(movies_dict)  # Convert the dictionary to a DataFrame

similarity = pickle.load(open('similarity.pkl', 'rb'))  # Load the similarity matrix

# Streamlit interface
st.title('Movie Recommender System')  # Set the title for the app

# Select a movie from the dropdown list
selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

# When the 'Recommend' button is clicked
if st.button('Recommend'):
    recommended_movies, recommended_movies_poster = recommend(selected_movie_name)  # Get recommendations and posters

    # Display the recommended movies in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movies_poster[0], caption=recommended_movies[0])
    with col2:
        st.image(recommended_movies_poster[1], caption=recommended_movies[1])
    with col3:
        st.image(recommended_movies_poster[2], caption=recommended_movies[2])
    with col4:
        st.image(recommended_movies_poster[3], caption=recommended_movies[3])
    with col5:
        st.image(recommended_movies_poster[4], caption=recommended_movies[4])
