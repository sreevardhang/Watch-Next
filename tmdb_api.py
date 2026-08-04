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

if __name__ == "__main__":
    title = input("Search for a movie: ")

    results = search_movies(title)

    for movie in results[:5]:
        print(movie["title"], movie.get("release_date", "Unknown date"))