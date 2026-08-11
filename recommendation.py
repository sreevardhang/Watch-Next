RESULT_LIMIT = 3

def calculate_scores(selected_movie, candidate_movies):
    scores = {}
    selected_genres = {genre.lower() for genre in selected_movie['genres']}
    selected_release_year = selected_movie['release_year']

    for movie in candidate_movies:
        movie_score = 0
        reasons = []
        candidate_genres = {genre.lower() for genre in movie['genres']}

        shared_genres = selected_genres.intersection(candidate_genres)

        movie_score += len(shared_genres) * 3

        if shared_genres:
            reasons.append(f"{', '.join(sorted(shared_genres))}")

        candidate_rating = movie.get('rating', 0)

        if candidate_rating >= 7.5:
            movie_score += 1
            reasons.append("highly rated")

        candidate_release_year = movie['release_year']
        if selected_release_year and candidate_release_year:
            year_diff = abs(selected_release_year - candidate_release_year)

            if year_diff <= 5:
                movie_score += 2
                reasons.append("similar release era (within 5 years)")
            elif year_diff <= 10:
                movie_score += 1
                reasons.append("similar release era (within 10 years)")
        

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