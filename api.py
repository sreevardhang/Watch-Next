from fastapi import FastAPI, HTTPException, status, Depends
from tmdb_api import search_movies, get_movie_details
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas import (
    RecommendationResponse,
    MovieSearchResponse,
    UserCreate,
    UserResponse,
    WatchlistCreate,
    WatchlistResponse,
    WatchedMovieCreate,
    WatchedMovieResponse
)
from recommendation_service import generate_recommendations
from database import get_db
from models import User, WatchlistItem, WatchedMovie

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
def create_user(user_data: UserCreate,
                session: Session = Depends(get_db)):
    user = User(name=user_data.name)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@app.post("/watchlist", response_model=WatchlistResponse)
def add_to_watchlist(movie_data: WatchlistCreate,
                     session: Session = Depends(get_db)):
    user = session.get(User, movie_data.user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found!"
        )
    movie = get_movie_details(movie_data.movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found!"
        )

    item = WatchlistItem(
        user_id=movie_data.user_id,
        movie_id=movie_data.movie_id,
        movie_title=movie['title']
    )

    try:
        session.add(item)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Movie already in watchlist!"
        )
    
    session.refresh(item)

    return item

@app.get("/watchlist/{user_id}", response_model=list[WatchlistResponse])
def get_watchlist(user_id: int,
                  session: Session = Depends(get_db)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found!"
        )

    statement = select(WatchlistItem).where(WatchlistItem.user_id == user_id)

    result = session.scalars(statement).all()

    return result

@app.delete("/watchlist/{user_id}/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_watchlistitem(user_id: int, movie_id: int,
                         session: Session = Depends(get_db)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found!"
        )
    
    statement = select(WatchlistItem).where(WatchlistItem.user_id == user_id,
                                            WatchlistItem.movie_id == movie_id)

    result = session.scalar(statement)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Movie not found in user's watchlist!"
        )
    
    session.delete(result)
    session.commit()

    return

@app.post("/watched", response_model=WatchedMovieResponse)
def add_watched_movie(movie_data: WatchedMovieCreate, session: Session = Depends(get_db)):
    user = session.get(User, movie_data.user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found!"
        )
    movie = get_movie_details(movie_data.movie_id)
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found!"
        )

    item = WatchedMovie(
        user_id=movie_data.user_id,
        movie_id=movie_data.movie_id,
        movie_title=movie['title']
    )

    try:
        session.add(item)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="You already watched this movie!"
        )
    session.refresh(item)

    return item

@app.get("/watched/{user_id}", response_model=list[WatchedMovieResponse])
def get_watched_movies(user_id: int, session: Session = Depends(get_db)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found!"
        )

    statement = select(WatchedMovie).where(WatchedMovie.user_id == user_id)

    result = session.scalars(statement).all()

    return result