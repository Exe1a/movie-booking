from pydantic import BaseModel, Field
from datetime import date, datetime

class Movie_model(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    release: date | None = None
    genre_id: int | None = None

    def get_fields(self) -> list:
        fields = []
        if self.id: fields.append("id")
        if self.title: fields.append("title")
        if self.description: fields.append("description")
        if self.release: fields.append("release")
        if self.genre_id: fields.append("genre_id")
        return fields
    
class Showtime_filter_model(BaseModel):
    id: int | None = None
    movie_id: int | None = None
    time: datetime | None = None

    def get_fields(self) -> list:
        fields = []
        if self.id: fields.append("id")
        if self.movie_id: fields.append("movie_id")
        if self.time: fields.append("time")
        return fields
    
class Showtime_model(BaseModel):
    movie_id: int
    time: datetime
    seats: int = Field(gt=0)

class User_form(BaseModel):
    login: str
    password: str