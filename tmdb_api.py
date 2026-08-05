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

if __name__ == "__main__":
    title = input("Search for a movie: ")

    results = search_movies(title)
    displayed_results = results[:5]
    genre_map = get_movie_genres()

    for index,movie in enumerate(displayed_results, start=1):
        print(f"{index}. {movie['title']} {movie.get('release_date', 'Unknown')}")

    while True:
        choice = input("Choose a movie number: ")

        if not choice.isdigit():
            print("Enter a number")
            continue
        choice_num = int(choice)
        if choice_num < 1 or choice_num > len(displayed_results):
            continue
        break

    selected_movie = displayed_results[choice_num - 1]

    movie_details = get_movie_details(selected_movie['id'])

    print(f"Title: {movie_details['title']}")
    print(f"Runtime: {movie_details.get('runtime', 'Unknown')} minutes")
    print(f"Overview: {movie_details.get('overview', 'No overview available')}")