from fastapi import APIRouter, Depends, Cookie
from sqlalchemy import select
from typing import Annotated
import json
from src.models.database import MoviesGenres
from src.database import get_session
from src.auth import admin_check
import src.cache as cache

router = APIRouter(prefix="/genre",
                   tags=["genre"])

@router.get(path="")
def list_genres(session = Depends(get_session)):
    cached_data = cache.redis.get("list_genres")
    if cached_data:
        return json.loads(cached_data)
    list_genres_not_prepared = session.scalars(select(MoviesGenres)).all()
    list_genres_prepared = dict()
    for genre in list_genres_not_prepared:
        list_genres_prepared[genre.id] = genre.genre
    cache.redis.set(name="list_genres",
                    value=json.dumps(list_genres_prepared),
                    ex=60*60)
    return list_genres_prepared

@router.post(path="")
def add_genre(new_genre: str,
              token: Annotated[str, Cookie()],
              session = Depends(get_session)):
    admin_check(token)
    genre = MoviesGenres(genre=new_genre)
    session.add(genre)
    session.commit()
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