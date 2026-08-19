from fastapi import FastAPI, HTTPException
from tmdb_api import search_movies
from sqlalchemy import select

from schemas import (
    RecommendationResponse,
    MovieSearchResponse,
    UserCreate,
    UserResponse
)
from recommendation_service import generate_recommendations
from database import SessionLocal
from models import User

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

    result = generate_recommendations(movie_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found!"
        )

    return result

@app.post("/users", response_model=UserResponse)
def create_user(user_data: UserCreate):
    with SessionLocal() as session:
        user = User(name=user_data.name)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user