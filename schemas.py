from pydantic import BaseModel

class RecommendationResponse(BaseModel):
    id: int
    title: str
    score: int
    reasons: list[str]

class MovieSearchResponse(BaseModel):
    id: int
    title: str
    release_date: str

class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str

class WatchlistCreate(BaseModel):
    user_id: int
    movie_id: int

class WatchlistResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    movie_title: str

class WatchedMovieCreate(BaseModel):
    movie_id: int
    user_id: int

class WatchedMovieResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    movie_title: str
