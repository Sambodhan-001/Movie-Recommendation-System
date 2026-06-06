import streamlit as st
import pandas as pd
import pickle

# Fetch poster from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US"

    response = requests.get(url)
    data = response.json()

    poster_path = data.get('poster_path')

    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


# Recommendation function
def recommend(selected_movie):
    
    # Find index of selected movie
    movie_index = movies[movies['title'] == selected_movie].index[0]

    # Get similarity scores
    distances = similarity[movie_index]

    # Get top 5 similar movies
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        # Movie title
        recommended_movies.append(movies.iloc[i[0]].title)

        # Poster
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies #recommended_movies_posters


# Load data
movie_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


# Streamlit UI
st.title('Movie Recommender System')

st.write(
    'This system recommends movies similar to your selected movie.'
)

selected_movie = st.selectbox(
    'Select a movie',
    movies['title'].values
)

# Recommend button
if st.button('Recommend'):

    recommended_movies = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movies[0])
        st.image(recommended_movies_posters[0])

    with col2:
        st.text(recommended_movies[1])
        st.image(recommended_movies_posters[1])

    with col3:
        st.text(recommended_movies[2])
        st.image(recommended_movies_posters[2])

    with col4:
        st.text(recommended_movies[3])
        st.image(recommended_movies_posters[3])

    with col5:
        st.text(recommended_movies[4])
        st.image(recommended_movies_posters[4])


