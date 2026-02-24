from pydantic import BaseModel, Field
from datetime import date, datetime

class MovieFilterModel(BaseModel):
    title: str | None = None
    release: date | None = None
    genre_id: int | None = None

class EditedMovieModel(MovieFilterModel):
    description: str | None = None

class NewMovieModel(BaseModel):
    title: str
    description: str
    release: date
    genre_id: int
    
class FilmSessionFilterModel(BaseModel):
    id: int | None = None
    movie_id: int | None = None
    time: datetime | None = None
    
class FilmSessionModel(BaseModel):
    movie_id: int
    time: datetime
    seats: int = Field(gt=0)

class UserForm(BaseModel):
    login: str
    password: str