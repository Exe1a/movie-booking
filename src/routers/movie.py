from fastapi import APIRouter, Query
from sqlalchemy import select
from typing import Annotated
from src.database import session_maker
from src.models.database import Movies
from src.models.pydantic_models import Movie_model

router = APIRouter(prefix="/movie", tags=["movie"])

@router.post("",summary="Get all movies or some movies by id/title/description/release/genre")
def get_movie(filter: Annotated[Movie_model, Query()]):
    fields = filter.get_fields()
    whr = []
    if "id" in fields: whr.append(Movies.id == filter.id)
    if "title" in fields: whr.append(Movies.title == filter.title)
    if "description" in fields: whr.append(Movies.description == filter.description)
    if "release" in fields: whr.append(Movies.release == filter.release)
    if "genre_id" in fields: whr.append(Movies.genre_id == filter.genre_id)
    with session_maker() as session:
        return session.scalars(select(Movies).where(*whr)).all()

@router.post("/add", summary="Add new movie in database")
def add_movie(new_movie: Annotated[Movie_model, Query()]):
    fileds = new_movie.get_fields()
    if "id" in fileds: return {"error": "id is not necessary"}
    if "title" not in fileds: return {"error": "title is necessary"}
    if "description" not in fileds: return {"error": "description is necessary"}
    if "release" not in fileds: return {"error": "release is necessary"}
    if "genre_id" not in fileds: return {"error": "genre_id is necessary"}
    movie = Movies(title = new_movie.title,
                   description = new_movie.description,
                   release = new_movie.release,
                   genre_id = new_movie.genre_id)
    with session_maker() as session:
        session.add(movie)
        session.commit()
    return {"result": "movie was added"}

@router.patch("/{movie_id}")
def edit_movie(movie_id: int, edited_movie: Annotated[Movie_model, Query()]):
    fields = edited_movie.get_fields()
    with session_maker() as session:
        movie_to_edit = session.scalar(select(Movies).where(Movies.id == movie_id))
        movie_to_edit.title = edited_movie.title if "title" in fields else movie_to_edit.title
        movie_to_edit.description = edited_movie.description if "description" in fields else movie_to_edit.description
        movie_to_edit.release = edited_movie.release if "release" in fields else movie_to_edit.release
        movie_to_edit.genre_id = edited_movie.genre_id if "genre_id" in fields else movie_to_edit.genre_id
        session.commit()
    return {"result" : "movie was edited"}

@router.delete("/{movie_id}")
def delete_movie(movie_id: int):
    with session_maker() as session:
        movie_to_delete = session.get(Movies, movie_id)
        session.delete(movie_to_delete)
        session.commit()
    return {"result": "movie was deleted"}