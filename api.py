from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tmdb_api import (
    search_movies,
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

class RecommendationResponse(BaseModel):
    id: int
    title: str
    score: int
    reasons: list[str]

class MovieSearchResponse(BaseModel):
    id: int
    title: str
    release_date: str

NUM_OF_CANDIDATES = 10

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get(
        "/movies/search",
        response_model=list[MovieSearchResponse])
def movie_search(query: str):
    results = search_movies(query)

    movies = []

    for movie in results[:5]:
        movies.append({
                "id": movie['id'],
                "title": movie['title'],
                "release_date": movie.get('release_date', '')
                })

    return movies

@app.get(
        "/recommendations/{movie_id}",
        response_model=list[RecommendationResponse]
        )
def recommendations(movie_id: int):

    genre_map = get_movie_genres()

    selected_details = get_movie_details(movie_id)

    if selected_details is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found!"
        )

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