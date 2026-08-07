import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")
BASE_URL = "https://api.themoviedb.org/3"

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

    response = requests.get(
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

    response = requests.get(
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

    response = requests.get(
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

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    return response.json()["results"]

def normalize_movie(movie, genre_map):
    if "genre_ids" in movie:
        genres = convert_genre_ids(movie.get('genre_ids',[]), genre_map)
    else:
        genres = [genre["name"] for genre in movie.get("genres",[])]

    return {
        "title": movie['title'],
        "type": "movie",
        "genres": genres,
        "rating": movie.get('vote_average',0),
        "runtime": movie.get('runtime', 'No runtime available'),
        "id": movie['id']
    }