from fastapi import APIRouter, Query, Depends, Cookie
from sqlalchemy import select
from typing import Annotated
from src.database import get_session
from src.models.database import Movies
from src.models.pydantic_models import MovieModel, InfoMovieModel
from src.utils import admin_check

router = APIRouter(prefix="/movie",
                   tags=["movie"])

@router.post(path="",
             summary="Get all movies or some movies by id/title/description/release/genre")
def get_movie(movie_filter: Annotated[InfoMovieModel, Query()],
              session = Depends(get_session)):
    fields = movie_filter.get_fields()
    whr = []
    if "id" in fields: whr.append(Movies.id == movie_filter.id)
    if "title" in fields: whr.append(Movies.title == movie_filter.title)
    if "description" in fields: whr.append(Movies.description == movie_filter.description)
    if "release" in fields: whr.append(Movies.release == movie_filter.release)
    if "genre_id" in fields: whr.append(Movies.genre_id == movie_filter.genre_id)
    return session.scalars(select(Movies).where(*whr)).all()

@router.post(path="/add",
             summary="Add new movie in database")
def add_movie(new_movie: Annotated[MovieModel, Query()],
              token: Annotated[str, Cookie()],
              session = Depends(get_session)):
    admin_check(token)
    movie = Movies(title = new_movie.title,
                   description = new_movie.description,
                   release = new_movie.release,
                   genre_id = new_movie.genre_id)
    session.add(movie)
    session.commit()
    return {"result": "movie was added"}

@router.patch(path="/{movie_id}")
def edit_movie(movie_id: int,
               edited_movie: Annotated[MovieModel, Query()],
               token: Annotated[str, Cookie()],
               session = Depends(get_session)):
    admin_check(token)
    fields = edited_movie.get_fields()
    movie_to_edit = session.get(Movies, movie_id)
    movie_to_edit.title = edited_movie.title if "title" in fields else movie_to_edit.title
    movie_to_edit.description = edited_movie.description if "description" in fields else movie_to_edit.description
    movie_to_edit.release = edited_movie.release if "release" in fields else movie_to_edit.release
    movie_to_edit.genre_id = edited_movie.genre_id if "genre_id" in fields else movie_to_edit.genre_id
    session.commit()
    return {"result" : "movie was edited"}

@router.delete(path="/{movie_id}")
def delete_movie(movie_id: int,
                 token: Annotated[str, Cookie()],
                 session = Depends(get_session)):
    admin_check(token)
    movie_to_delete = session.get(Movies, movie_id)
    session.delete(movie_to_delete)
    session.commit()
    return {"result": "movie was deleted"}