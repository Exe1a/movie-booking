from fastapi import APIRouter, Depends, Cookie
from sqlalchemy import select
from typing import Annotated
import json
from src.database import get_session
from src.models.database import Movies
from src.models.pydantic_models import EditedMovieModel, MovieFilterModel, NewMovieModel
from src.auth import admin_check
import src.cache as cache

router = APIRouter(prefix="/movie",
                   tags=["movie"])

@router.get(path="")
def get_all_movie(session=Depends(get_session)):
    cached_data = cache.redis.hgetall("movie:all").items()
    if cached_data:
        return {movie_id: json.loads(fields) for movie_id, fields in cached_data}
    all_movie_data = session.scalars(select(Movies)).all()
    all_movie_prepared_data = {f"{movie.id}" : {"title": movie.title,
                                                "description": movie.description,
                                                "release": str(movie.release),
                                                "genre_id": str(movie.genre_id)} for movie in all_movie_data}
    cache.redis.hset(name="movie:all",
                     mapping={f"{movie_id}": json.dumps(fields) for movie_id, fields in all_movie_prepared_data.items()})
    return all_movie_prepared_data
    

@router.get(path="/{id}")
def get_movie_by_id(movie_id: int,
                    session = Depends(get_session)):
    cached_data = cache.redis.hgetall(name=f"movie:{movie_id}")
    if cached_data:
        return cached_data
    movie_data = session.scalar(select(Movies).where(Movies.id == movie_id))
    movie_prepared_data = {"title": movie_data.title,
                           "description": movie_data.description,
                           "release": str(movie_data.release),
                           "genre_id": str(movie_data.genre_id)}
    cache.redis.hset(name=f"movie:{movie_id}",
                     mapping=movie_prepared_data)
    return movie_prepared_data
    
@router.post(path="")
def get_movie_with_filter(movie_filter: MovieFilterModel,
                          session = Depends(get_session)):
    whr = []
    if movie_filter.title: whr.append(Movies.title == movie_filter.title)
    if movie_filter.release: whr.append(Movies.release == movie_filter.release)
    if movie_filter.genre_id: whr.append(Movies.genre_id == movie_filter.genre_id)
    movies_data = session.scalars(select(Movies).where(*whr)).all()
    movies_data_prepared = {f"{movie.id}": {"title": movie.title,
                                            "description": movie.description,
                                            "release": str(movie.release),
                                            "genre_id": str(movie.genre_id)} for movie in movies_data}
    return movies_data_prepared

@router.post(path="/add")
def add_movie(new_movie: NewMovieModel,
              token: Annotated[str, Cookie()],
              session = Depends(get_session)):
    admin_check(token)
    movie = Movies(title = new_movie.title,
                   description = new_movie.description,
                   release = new_movie.release,
                   genre_id = new_movie.genre_id)
    session.add(movie)
    session.commit()
    keys_to_delete = cache.redis.keys("movie:*")
    if keys_to_delete:
        cache.redis.delete(*keys_to_delete)
    return {"result": "movie was added"}

@router.patch(path="/{movie_id}")
def edit_movie(movie_id: int,
               edited_movie: EditedMovieModel,
               token: Annotated[str, Cookie()],
               session = Depends(get_session)):
    admin_check(token)
    movie_to_edit = session.get(Movies, movie_id)
    if edited_movie.title: movie_to_edit.title = edited_movie.title
    if edited_movie.description: movie_to_edit.description = edited_movie.description
    if edited_movie.release: movie_to_edit.release = edited_movie.release
    if edited_movie.genre_id: movie_to_edit.genre_id = edited_movie.genre_id
    session.commit()
    keys_to_delete = cache.redis.keys("movie:*")
    if keys_to_delete:
        cache.redis.delete(*keys_to_delete)
    return {"result" : "movie was edited"}

@router.delete(path="/{movie_id}")
def delete_movie(movie_id: int,
                 token: Annotated[str, Cookie()],
                 session = Depends(get_session)):
    admin_check(token)
    movie_to_delete = session.get(Movies, movie_id)
    session.delete(movie_to_delete)
    session.commit()
    keys_to_delete = cache.redis.keys("movie:*")
    if keys_to_delete:
        cache.redis.delete(*keys_to_delete)
    return {"result": "movie was deleted"}