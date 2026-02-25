from fastapi import APIRouter, Depends, Cookie
from sqlalchemy import select
from sqlalchemy.orm import Session
from redis import Redis
from typing import Annotated
from src.database.models import MoviesGenres
from src.database.orm import get_session
from src.database.cache import get_redis
from src.auth import admin_check

router = APIRouter(prefix="/genre",
                   tags=["genre"])

@router.get(path="")
def list_genres(session: Session = Depends(get_session),
                cache: Redis = Depends(get_redis)):
    cached_data = cache.hgetall("list_genres")
    if cached_data:
        return cached_data
    list_genres_data = session.scalars(select(MoviesGenres)).all()
    list_genres_prepared_data = {genre.id: genre.genre for genre in list_genres_data}
    cache.hset(name="list_genres",
               mapping=list_genres_prepared_data)
    return list_genres_prepared_data

@router.post(path="")
def add_genre(new_genre: str,
              token: Annotated[str, Cookie()],
              session = Depends(get_session),
              cache = Depends(get_redis)):
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
               session = Depends(get_session),
               cache = Depends(get_redis)):
    admin_check(token)
    genre_obj = session.scalar(select(MoviesGenres).where(MoviesGenres.id == genre_id))
    genre_obj.genre = genre_new_name
    session.commit()
    cache.redis.delete("list_genres")
    return {"result":"genre was renamed"}

@router.delete(path="/{genre_id}")
def delete_genre(genre_id: int,
                 token: Annotated[str, Cookie()],
                 session = Depends(get_session),
                 cache = Depends(get_redis)):
    admin_check(token)
    genre_to_delete = session.get(MoviesGenres, genre_id)
    session.delete(genre_to_delete)
    session.commit()
    cache.redis.delete("list_genres")
    return {"result":"genre with movies was deleted"}