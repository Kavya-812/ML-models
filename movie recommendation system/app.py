import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=78ecc5ae87321af1f7e050eae35db1c2&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return None


def recommend(movie):
    if movie not in movies['title'].values:
        return ["Movie not found"], [None] * 5, [None] * 5

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []
    for i in distances[1:6]:
        # fetch the movie poster
        poster_path = fetch_poster(movies.iloc[i[0]]['id'])
        if poster_path:
            recommended_movie_posters.append(poster_path)
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_ids.append(movies.iloc[i[0]]['id'])

    return recommended_movie_names, recommended_movie_posters, recommended_movie_ids


st.title('Movie Recommender System')
st.subheader('Creator-Kavya')
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_ids = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])


st.markdown('[Click here to get to know the developer](https://github.com/Kavya-812)')

