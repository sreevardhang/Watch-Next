from tmdb_api import (
    get_movie_details,
    get_movie_keywords,
    get_tmdb_recommendations,
    normalize_movie,
    get_movie_genres,
)
from recommendation import (
    calculate_scores,
    get_recommendations
)

NUM_OF_CANDIDATES = 10

def generate_recommendations(movie_id):
    genre_map = get_movie_genres()

    selected_details = get_movie_details(movie_id)

    if selected_details is None:
        return None

    selected_keywords = get_movie_keywords(movie_id)

    norm_selected_movie = normalize_movie(selected_details, selected_keywords, genre_map)

    candidates = get_tmdb_recommendations(movie_id)[:NUM_OF_CANDIDATES]

    norm_candidates = []
    for candidate in candidates:
        candidate_keywords = get_movie_keywords(candidate['id'])
        norm_candidates.append(normalize_movie(candidate, candidate_keywords, genre_map))

    scores = calculate_scores(norm_selected_movie, norm_candidates)

    recommendations = get_recommendations(scores)

    recommendation_result = []
    for item in recommendations:
        recommendation_result.append({
            "id": item['movie_details']['id'],
            "title": item['title'],
            "score": item['score'],
            "reasons": item['reasons']         
        })

    return recommendation_result