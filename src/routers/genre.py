from fastapi import APIRouter, Depends, Cookie
from sqlalchemy import select
from typing import Annotated
from src.models.database import MoviesGenres
from src.database import get_session
from src.utils import admin_check

router = APIRouter(prefix="/genre",
                   tags=["genre"],
                   )

@router.get(path="")
def list_genres(token: Annotated[str, Cookie()],
                session = Depends(get_session)):
    admin_check(token)
    return session.scalars(select(MoviesGenres)).all()

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
    return {"result":"genre was renamed"}

@router.delete(path="/{genre_id}")
def delete_genre(genre_id: int,
                 token: Annotated[str, Cookie()],
                 session = Depends(get_session)):
    admin_check(token)
    genre_to_delete = session.get(MoviesGenres, genre_id)
    session.delete(genre_to_delete)
    session.commit()
    return {"result":"genre with movies was deleted"}