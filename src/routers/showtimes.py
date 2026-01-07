from fastapi import APIRouter, Query
from sqlalchemy import select
from typing import Annotated
from src.models.pydantic_models import Showtime_filter_model, Showtime_model
from src.models.database import Showtimes
from src.database import session_maker

router = APIRouter(prefix="/showtimes", tags=["showtimes"])

@router.post("")
def list_showtimes(filter: Annotated[Showtime_filter_model, Query()]):
    fields = filter.get_fields()
    whr = []
    if "id" in fields: whr.append(Showtimes.id == filter.id)
    if "movie_id" in fields: whr.append(Showtimes.movie_id == filter.movie_id)
    if "time" in fields: whr.append(Showtimes.time == filter.time)
    with session_maker() as session:
        return session.scalars(select(Showtimes).where(*whr)).all()
    
@router.post("/add")
def add_showtime(showtime: Annotated[Showtime_model, Query()]):
    new_showtime = Showtimes(movie_id=showtime.movie_id,
                             time = showtime.time,
                             seats=showtime.seats)
    with session_maker() as session:
        session.add(new_showtime)
        session.commit()
    return {"result": "showtime was added"}

@router.delete("")
def delete_showtime(id: int):
    with session_maker() as session:
        showtime = session.get(Showtimes, id)
        session.delete(showtime)
        session.commit()
    return {"result": "showtime was deleted"}