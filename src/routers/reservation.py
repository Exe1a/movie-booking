from fastapi import APIRouter
from sqlalchemy import select
from src.database import session_maker
from src.models.database import Reservation, Showtimes

router = APIRouter(prefix="/reservation", tags=["reservation"])

@router.post("")
def list_reservation(showtime_id: int | None = None,
                     user_id: int | None = None):
    whr = []
    if showtime_id: whr.append(showtime_id == Reservation.showtime_id)
    if user_id: whr.append(user_id == Reservation.user_id)
    with session_maker() as session:
        return session.scalars(select(Reservation).where(*whr)).all()

@router.post("/add")
def add_reservation(showtime_id: int | None = None,
                    user_id: int | None = None):
    new_reservation = Reservation(showtime_id = showtime_id,
                                  user_id = user_id)
    with session_maker() as session:
        session.add(new_reservation)
        showtime = session.get(Showtimes, showtime_id)
        showtime.reserved += 1
        session.commit()
    return {"result" : "Showtime was added"}

@router.delete("")
def delete_reservation(id: int):
    with session_maker() as session:
        reserv = session.get(Reservation, id)
        session.delete(reserv)
        showtime = session.get(Showtimes, reserv.showtime_id)
        showtime.reserved -= 1
        session.commit()
    return {"result": "Reservatoin was deleted"}