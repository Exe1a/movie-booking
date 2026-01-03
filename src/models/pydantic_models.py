from pydantic import BaseModel
from datetime import date

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