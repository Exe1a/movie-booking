from fastapi import APIRouter, Query
from sqlalchemy import select
from typing import Annotated
from src.database import session_maker
from src.models import Movies, Movie_model

router = APIRouter(prefix="/movie", tags=["movie"])

@router.post("", summary="Get all movies or some movies by id/title/description/release/genre")
def get_movie(filter: Annotated[Movie_model, Query()]):
    fields = filter.get_fields()
    whr = []
    if "id" in fields: whr.append(Movies.id == filter.id)
    if "title" in fields: whr.append(Movies.title == filter.title)
    if "description" in fields: whr.append(Movies.description == filter.description)
    if "release" in fields: whr.append(Movies.release == filter.release)
    if "genre" in fields: whr.append(Movies.genre == filter.genre)
    with session_maker() as session:
        return session.scalars(select(Movies).where(*whr)).all()

@router.post("/add", summary="Add new movie in database")
def add_movie(movie: Annotated[Movie_model, Query()]):
    fileds = movie.get_fields()
    if "id" in fileds: return {"error": "id is not necessary"}
    if "title" not in fileds: return {"error": "title is necessary"}
    if "description" not in fileds: return {"error": "description is necessary"}
    if "release" not in fileds: return {"error": "release is necessary"}
    if "genre" not in fileds: return {"error": "genre is necessary"}
    new_movie = Movies(title = movie.title,
                       description = movie.description,
                       release = movie.release,
                       genre = movie.genre)
    with session_maker() as session:
        session.add(new_movie)
        session.commit()
    return {"result": "movie was added"}