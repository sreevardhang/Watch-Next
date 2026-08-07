from tmdb_api import(
    search_movies,
    get_movie_genres,
    get_movie_details,
    get_tmdb_recommendations,
    normalize_movie,
)

from recommendation import(
    calculate_scores,
    get_recommendations
)

if __name__ == "__main__":

    while True:
        title = input("Search for a movie: ")
        results = search_movies(title)
        if not results:
            print("No such movie found! Try again!\n")
            continue
        break

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

    scores = calculate_scores(selected_normalized, candidates_normalized)

    recommendations = get_recommendations(scores)

    print(f"Because you liked {selected_normalized['title']}:\n")

    for title, details in recommendations:
        print(title)
        print(f"Similarity Score: {details['score']}")
        print(f"Reasons: {', '.join(details['reasons'])}")
        print("-" * 40)