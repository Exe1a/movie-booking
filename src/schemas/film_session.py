from pydantic import BaseModel, Field
from datetime import datetime

class FilmSessionFilterSchema(BaseModel):
    id: int | None = None
    movie_id: int | None = None
    time: datetime | None = None
    
class FilmSessionSchema(BaseModel):
    movie_id: int
    time: datetime
    seats: int = Field(gt=0)