from fastapi import APIRouter, Depends, Cookie
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated
from redis import Redis
from src.schemas.film_session import FilmSessionFilterModel, FilmSessionModel
from src.database.models import FilmSession
from src.database.orm import get_session
from src.auth import admin_check

router = APIRouter(prefix="/film-session",
                   tags=["film-session"])

@router.post(path="")
def list_film_sessions(film_session_filter: FilmSessionFilterModel,
                       session: Session = Depends(get_session)):
    whr = []
    if film_session_filter.id: whr.append(FilmSession.id == film_session_filter.id)
    if film_session_filter.movie_id: whr.append(FilmSession.movie_id == film_session_filter.movie_id)
    if film_session_filter.time: whr.append(FilmSession.time == film_session_filter.time)
    return session.scalars(select(FilmSession).where(*whr)).all()
    
@router.post(path="/add")
def add_film_session(film_session: FilmSessionModel,
                     token: Annotated[str, Cookie()],
                     session: Session = Depends(get_session)):
    admin_check(token)
    new_film_session = FilmSession(movie_id=film_session.movie_id,
                                   time = film_session.time,
                                   seats=film_session.seats)
    session.add(new_film_session)
    session.commit()
    return {"result": "Film session was added"}

@router.delete(path="/{film_session_id}")
def delete_film_session(film_session_id: int,
                        token: Annotated[str, Cookie()],
                        session: Session = Depends(get_session)):
    admin_check(token)
    film_session = session.get(FilmSession, film_session_id)
    session.delete(film_session)
    session.commit()
    return {"result": "Film session was deleted"}