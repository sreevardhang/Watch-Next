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