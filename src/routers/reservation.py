from typing import Annotated
from fastapi import APIRouter, Cookie, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
import json
from src.database import get_session
from src.models.database import Reservation, FilmSession
from src.auth import get_user_id
import src.cache as cache

router = APIRouter(prefix="/reservation",
                   tags=["reservation"])

@router.post("")
def list_reservation(token: Annotated[str, Cookie()],
                     session = Depends(get_session)):
    user_id = get_user_id(token)
    cached_data = cache.redis.hgetall(f"reservation:{user_id}").items()
    if cached_data:
        cached_data_prepared = {reserv_id: json.loads(data) for reserv_id, data in cached_data}
        return cached_data_prepared
    reservation_data = session.scalars(select(Reservation).where(Reservation.user_id == user_id)).all()
    reservation_data_prepared = {reserv.id: {"film_session_id": reserv.film_session_id,
                                             "user_id": reserv.user_id} for reserv in reservation_data}
    cache.redis.hset(name=f"reservation:{user_id}",
                     mapping={reserv_id: json.dumps(data) for reserv_id, data in reservation_data_prepared.items()})
    return reservation_data_prepared

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
    cache.redis.delete(f"reservation:{user_id}")
    return {"result" : "Reservation was added"}

@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int,
                       token: Annotated[str, Cookie()],
                       session = Depends(get_session)):
    user_id = get_user_id(token)
    reservation = session.get(Reservation, reservation_id)
    if user_id != reservation.user_id:
        raise HTTPException(403, "It's not your reservation")
    session.delete(reservation)
    film_session = session.get(FilmSession, reservation.film_session_id)
    film_session.reserved -= 1
    session.commit()
    cache.redis.delete(f"reservation:{user_id}")
    return {"result": "Reservation was deleted"}