from fastapi import APIRouter, Query, Depends, Cookie
from sqlalchemy import select
from typing import Annotated
from src.models.pydantic_models import Showtime_filter_model, Showtime_model
from src.models.database import Showtimes
from src.database import get_session
from src.utils import admin_check

router = APIRouter(prefix="/showtimes", tags=["showtimes"])

@router.post("")
def list_showtimes(showtime_filter: Annotated[Showtime_filter_model, Query()],
                   session = Depends(get_session)):
    fields = showtime_filter.get_fields()
    whr = []
    if "id" in fields: whr.append(Showtimes.id == showtime_filter.id)
    if "movie_id" in fields: whr.append(Showtimes.movie_id == showtime_filter.movie_id)
    if "time" in fields: whr.append(Showtimes.time == showtime_filter.time)
    return session.scalars(select(Showtimes).where(*whr)).all()
    
@router.post("/add")
def add_showtime(showtime: Annotated[Showtime_model, Query()],
                 token: Annotated[str, Cookie()],
                 session = Depends(get_session)):
    Depends(admin_check(token))
    new_showtime = Showtimes(movie_id=showtime.movie_id,
                             time = showtime.time,
                             seats=showtime.seats)
    session.add(new_showtime)
    session.commit()
    return {"result": "showtime was added"}

@router.delete("/{showtime_id}")
def delete_showtime(showtime_id: int,
                    token: Annotated[str, Cookie()],
                    session = Depends(get_session)):
    Depends(admin_check(token))
    showtime = session.get(Showtimes, showtime_id)
    session.delete(showtime)
    session.commit()
    return {"result": "showtime was deleted"}