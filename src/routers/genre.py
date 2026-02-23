from fastapi import APIRouter, Depends, Cookie
from sqlalchemy import select
from typing import Annotated
from src.models.database import MoviesGenres
from src.database import get_session
from src.auth import admin_check
import src.cache as cache

router = APIRouter(prefix="/genre",
                   tags=["genre"])

@router.get(path="")
def list_genres(session = Depends(get_session)):
    cached_data = cache.redis.hgetall("list_genres")
    if cached_data:
        return cached_data
    list_genres_data = session.scalars(select(MoviesGenres)).all()
    list_genres_prepared_data = {f"{genre.id}": genre.genre for genre in list_genres_data}
    cache.redis.hset(name="list_genres",
                     mapping=list_genres_prepared_data)
    return list_genres_prepared_data

@router.post(path="")
def add_genre(new_genre: str,
              token: Annotated[str, Cookie()],
              session = Depends(get_session)):
    admin_check(token)
    genre = MoviesGenres(genre=new_genre)
    session.add(genre)
    session.commit()
    cache.redis.delete("list_genres")
    return {"result":"genre was added"}

@router.patch(path="/{genre_id}")
def edit_genre(genre_id: int,
               genre_new_name: str,
               token: Annotated[str, Cookie()],
               session = Depends(get_session)):
    admin_check(token)
    genre_obj = session.scalar(select(MoviesGenres).where(MoviesGenres.id == genre_id))
    genre_obj.genre = genre_new_name
    session.commit()
    cache.redis.delete("list_genres")
    return {"result":"genre was renamed"}

@router.delete(path="/{genre_id}")
def delete_genre(genre_id: int,
                 token: Annotated[str, Cookie()],
                 session = Depends(get_session)):
    admin_check(token)
    genre_to_delete = session.get(MoviesGenres, genre_id)
    session.delete(genre_to_delete)
    session.commit()
    cache.redis.delete("list_genres")
    return {"result":"genre with movies was deleted"}