from pydantic import BaseModel
from datetime import date

class MovieFilterSchema(BaseModel):
    title: str | None = None
    release: date | None = None
    genre_id: int | None = None

class EditedMovieSchema(MovieFilterSchema):
    description: str | None = None

class NewMovieSchema(BaseModel):
    title: str
    description: str
    release: date
    genre_id: int