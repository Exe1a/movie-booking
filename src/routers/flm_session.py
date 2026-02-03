from fastapi import APIRouter, Query, Depends, Cookie
from sqlalchemy import select
from typing import Annotated
from src.models.pydantic_models import FilmSessionFilterModel, FilmSessionModel
from src.models.database import FilmSession
from src.database import get_session
from src.utils import admin_check

router = APIRouter(prefix="/film-session",
                   tags=["film-session"])

@router.post(path="")
def list_film_sessions(film_session_filter: Annotated[FilmSessionFilterModel, Query()],
                       session = Depends(get_session)):
    fields = film_session_filter.get_fields()
    whr = []
    if "id" in fields: whr.append(FilmSession.id == film_session_filter.id)
    if "movie_id" in fields: whr.append(FilmSession.movie_id == film_session_filter.movie_id)
    if "time" in fields: whr.append(FilmSession.time == film_session_filter.time)
    return session.scalars(select(FilmSession).where(*whr)).all()
    
@router.post(path="/add")
def add_film_session(film_session: Annotated[FilmSessionModel, Query()],
                     token: Annotated[str, Cookie()],
                     session = Depends(get_session)):
    admin_check(token)
    new_film_session = FilmSession(movie_id=film_session.movie_id,
                               time = film_session.time,
                               seats=film_session.seats)
    session.add(new_film_session)
    session.commit()
    return {"result": "Film session was added"}

@router.delete(path="/{film_session_id}")
def delete_showtime(film_session_id: int,
                    token: Annotated[str, Cookie()],
                    session = Depends(get_session)):
    admin_check(token)
    film_session = session.get(FilmSession, film_session_id)
    session.delete(film_session)
    session.commit()
    return {"result": "Film session was deleted"}