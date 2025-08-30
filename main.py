import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = 'https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1'


@st.cache_data
def get_metadata(title, type_="movie"):
    if type_ == "movie":
        url = f"https://api.themoviedb.org/3/search/movie?api_key=6a60b59afb2559526040579aa60765c3&query={title}"
    else:  # TV shows
        url = f"https://api.themoviedb.org/3/search/tv?api_key=6a60b59afb2559526040579aa60765c3&query={title}"

    response = requests.get(url)
    data = response.json()

    if data['results']:
        item = data['results'][0]  # first result
        metadata = {
            'title': item.get('name') if type_ == "tv" else item.get('title'),
            'release_date': item.get('first_air_date') if type_ == "tv" else item.get('release_date'),
            'rating': item.get('vote_average'),
            'overview': item.get('overview'),
            'poster_path': f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get(
                'poster_path') else None,
            'id': item.get('id')
        }
        return metadata
    return None



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    dist = similarity[movie_index]
    movies_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]


    recommended_movies = []
    for i in movies_list:
        movie_id = i[0]

        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

movies_dist = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_dist
                      )

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie/TV show recommender system')

select_movie_name = st.selectbox('Choose a movie/tv show',
                       movies['title'].values)

if st.button("Recommend"):
    recommendations = recommend(select_movie_name)
    st.write(f"Top {len(recommendations)} recommendations for **{select_movie_name}**:")

    for rec in recommendations:
        # Determine if it's a movie or TV show
        rec_type = movies[movies['title'] == rec]['type'].values[0].lower()  # "movie" or "tv show"
        type_ = "tv" if rec_type == "tv show" else "movie"

        meta = get_metadata(rec, type_=type_)
        if meta:
            st.image(meta['poster_path'], width=150)
            st.write(f"**{meta['title']}** ({meta['release_date'][:4] if meta['release_date'] else 'N/A'})")
            st.write(f"Rating: {meta['rating']}")
            st.write(meta['overview'])
            st.write("---")
        else:
            st.write(f"**{rec}** — Metadata not found")


#SIDEBAR FILTERS

st.sidebar.title("Filters")

# Filter by type
type_filter = st.sidebar.multiselect(
    "Select type",
    options=movies['type'].unique(),
    default=movies['type'].unique(),
    key="type_filter"
)

# Filter by minimum rating
min_rating = st.sidebar.slider(
    "Minimum rating",
    min_value=0.0,
    max_value=10.0,
    value=0.0,
    step=0.1
)

# Apply filters
filtered_movies = movies[(movies['type'].isin(type_filter)) &
                         (movies.get('rating', 0) >= min_rating)]





