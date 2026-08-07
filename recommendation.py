RESULT_LIMIT = 3

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