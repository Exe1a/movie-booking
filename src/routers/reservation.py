from typing import Annotated
from fastapi import APIRouter, Cookie, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from src.database import get_session
from src.models.database import Reservation, FilmSession
from src.utils import get_user_id

router = APIRouter(prefix="/reservation",
                   tags=["reservation"])

@router.post("")
def list_reservation(token: Annotated[str, Cookie()],
                     session = Depends(get_session)):
    user_id = get_user_id(token)
    return session.scalars(select(Reservation).where(Reservation.user_id == user_id)).all()

@router.post("/add")
def add_reservation(film_session_id: int,
                    token: Annotated[str, Cookie()],
                    session = Depends(get_session)):
    user_id = get_user_id(token)
    new_reservation = Reservation(film_session_id = film_session_id,
                                  user_id = user_id)
    session.add(new_reservation)
    showtime = session.get(FilmSession, film_session_id)
    showtime.reserved += 1
    session.commit()
    return {"result" : "Film session was added"}

@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int,
                       token: Annotated[str, Cookie()],
                       session = Depends(get_session)):
    reservation = session.get(Reservation, reservation_id)
    if get_user_id(token) != reservation.user_id:
        raise HTTPException(403, "It's not your reservation")
    session.delete(reservation)
    film_session = session.get(FilmSession, reservation.film_session_id)
    film_session.reserved -= 1
    session.commit()
    return {"result": "Reservation was deleted"}