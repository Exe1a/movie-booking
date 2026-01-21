from typing import Annotated
from fastapi import APIRouter, Cookie
from fastapi.params import Depends
from sqlalchemy import select
from src.database import get_session
from src.models.database import Reservation, Showtimes
from src.utils import admin_check

router = APIRouter(prefix="/reservation", tags=["reservation"])

@router.post("")
def list_reservation(showtime_id: int | None = None,
                     user_id: int | None = None,
                     session = Depends(get_session)):
    whr = []
    if showtime_id: whr.append(showtime_id == Reservation.showtime_id)
    if user_id: whr.append(user_id == Reservation.user_id)
    return session.scalars(select(Reservation).where(*whr)).all()

@router.post("/add")
def add_reservation(showtime_id: int | None = None,
                    user_id: int | None = None,
                    *,
                    token: Annotated[str, Cookie()],
                    session = Depends(get_session)):
    Depends(admin_check(token))
    new_reservation = Reservation(showtime_id = showtime_id,
                                  user_id = user_id)
    session.add(new_reservation)
    showtime = session.get(Showtimes, showtime_id)
    showtime.reserved += 1
    session.commit()
    return {"result" : "Showtime was added"}

@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int,
                       token: Annotated[str, Cookie()],
                       session = Depends(get_session)):
    Depends(admin_check(token))
    reservation = session.get(Reservation, reservation_id)
    session.delete(reservation)
    showtime = session.get(Showtimes, reservation.showtime_id)
    showtime.reserved -= 1
    session.commit()
    return {"result": "Reservation was deleted"}