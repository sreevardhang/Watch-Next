import os
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")
BASE_URL = "https://api.themoviedb.org/3"
retry_strategy = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429,500,502,503,504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session = requests.Session()

session.mount("https://", adapter)

def search_movies(query):
    url = f"{BASE_URL}/search/movie"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "accept": "application/json"
    }

    params = {
        "query": query,
        "include_adult": "false",
        "language": "en-US",
        "page": 1
    }

    response = session.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()["results"]

def get_movie_genres():
    url = f"{BASE_URL}/genre/movie/list"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "accept": "application/json"
    }

    response = session.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    genres = response.json()['genres']

    return {
        genre['id']: genre['name']
        for genre in genres
    }

def convert_genre_ids(genre_ids, genre_map):
    genre_names = []

    for genre_id in genre_ids:
        if genre_id in genre_map:
            genre_names.append(genre_map[genre_id])

    return genre_names    

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "accept": "application/json"
    }

    response = session.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    return response.json()

def get_tmdb_recommendations(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/recommendations"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "accept": "application/json"
    }

    response = session.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    return response.json()["results"]

def normalize_movie(movie, keywords, genre_map):
    if "genre_ids" in movie:
        genres = convert_genre_ids(movie.get('genre_ids',[]), genre_map)
    else:
        genres = [genre["name"] for genre in movie.get("genres",[])]

    release_date = movie.get('release_date','')

    if release_date:
        release_year = int(release_date[:4])
    else:
        release_year = None

    return {
        "title": movie['title'],
        "type": "movie",
        "genres": genres,
        "keywords": keywords,
        "rating": movie.get('vote_average',0),
        "release_year": release_year,
        "runtime": movie.get('runtime', 'No runtime available'),
        "id": movie['id']
    }

def get_movie_keywords(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/keywords"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "accept": "application/json"
    }

    response = session.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    keywords = response.json()

    movie_keywords = []

    for keyword in keywords["keywords"]:
        movie_keywords.append(keyword['name'])

    return movie_keywords

# if __name__ == "__main__":

#     genre_map = get_movie_genres()

#     # movie = get_movie_details(231)

#     # norm_movie = normalize_movie(movie, genre_map)

#     keywords = get_movie_keywords(231)

#     print(keywords)