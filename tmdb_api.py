import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")
BASE_URL = "https://api.themoviedb.org/3"
RESULT_LIMIT = 3

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

def calculate_scores(selected_movie, candidate_movies):
    scores = {}
    selected_genres = {genre.lower() for genre in selected_movie['genres']}

    for movie in candidate_movies:
        movie_score = 0
        reasons = []
        candidate_genres = {genre.lower() for genre in movie['genres']}

        shared_genres = selected_genres.intersection(candidate_genres)

        movie_score += len(shared_genres) * 2

        if shared_genres:
            reasons.append(f"{', '.join(sorted(shared_genres))}")

        candidate_rating = movie.get('rating', 0)

        if candidate_rating >= 7:
            movie_score += 1
            reasons.append("highly rated")

        scores[movie['title']] = {'score': movie_score, 'reasons': reasons, 'movie': movie}

    return scores

def get_recommendations(scores):
    positive_scores = {
        title: details
        for title, details in scores.items()
        if details['score'] > 0
    }

    sorted_scores = sorted(
        positive_scores.items(),
        key=lambda pair: pair[1]['score'],
        reverse = True
    )

    return sorted_scores[:RESULT_LIMIT]

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

    selected_normalized = normalize_movie(movie_details, genre_map)

    candidates = get_tmdb_recommendations(selected_movie["id"])

    candidates_normalized = [normalize_movie(movie, genre_map) for movie in candidates]

    # print("\nSelected Normalized: ")
    # print(selected_normalized)

    # print("\nCandidates Normalized: ")
    # for movie in candidates_normalized[:3]:
    #     print(movie)


    scores = calculate_scores(selected_normalized, candidates_normalized)

    recommendations = get_recommendations(scores)

    print(f"Because you liked {selected_normalized['title']}:\n")

    for title, details in recommendations:
        print(title)
        print(f"Similarity Score: {details['score']}")
        print(f"Reasons: {details['reasons']}")
        print("-" * 40)


