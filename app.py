import pickle
import streamlit as st
import requests

# Load movie data and similarity matrix
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))


# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:11]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Streamlit app
st.set_page_config(page_title="Movie recommendation System", page_icon=":clapper:", layout="wide")

# Header section
st.header("Movie recommendation  System Using Machine Learning")
st.write("")

# Movie selection section
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list,
    help="Select a movie to get recommendations"
)

# Button to show recommendations
if st.button('Show Recommendation'):
    with st.spinner("Loading recommendations..."):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommendations
    st.write("")
    st.header("Recommended Movies")
    cols = st.columns(5)
    for i, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
        with cols[i % 5]:
            st.image(poster, use_column_width=True)
            st.write(f"**{name}**")

# Add a footer section
footer = """
<style>
a:link , a:visited{
    color: blue;
    background-color: transparent;
    text-decoration: underline;
}

a:hover,  a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f5f5f5;
    color: #333;
    text-align: center;
    padding: 10px;
    border-top: 1px solid #ddd;
}
</style>

<div class="footer">
    <p>Made with ❤️ by AA</p>
    <div class="loader"></div>
</div>
"""

st.write(footer, unsafe_allow_html=True)