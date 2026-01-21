from fastapi import APIRouter, Depends, Cookie
from sqlalchemy import select
from typing import Annotated
from src.models.database import Movies_Genres
from src.database import get_session
from src.utils import admin_check

router = APIRouter(prefix="/genre", tags=["genre"])

@router.get("")
def list_genres(token: Annotated[str, Cookie()],
                session = Depends(get_session)):
    Depends(admin_check(token))
    return session.scalars(select(Movies_Genres)).all()

@router.post("")
def add_genre(new_genre: str,
              token: Annotated[str, Cookie()],
              session = Depends(get_session)):
    Depends(admin_check(token))
    genre = Movies_Genres(genre=new_genre)
    session.add(genre)
    session.commit()
    return {"result":"genre was added"}

@router.patch("/{genre_id}")
def edit_genre(genre_id: int,
               genre_new_name: str,
               token: Annotated[str, Cookie()],
               session = Depends(get_session)):
    Depends(admin_check(token))
    genre_obj = session.scalar(select(Movies_Genres).where(Movies_Genres.id == genre_id))
    genre_obj.genre = genre_new_name
    session.commit()
    return {"result":"genre was renamed"}

@router.delete("/{genre_id}")
def delete_genre(genre_id: int,
                 token: Annotated[str, Cookie()],
                 session = Depends(get_session)):
    Depends(admin_check(token))
    genre_to_delete = session.get(Movies_Genres, genre_id)
    session.delete(genre_to_delete)
    session.commit()
    return {"result":"genre with movies was deleted"}