from fastapi import APIRouter, Query
from sqlalchemy import select
from typing import Annotated
from src.database import session_maker
from src.models import Movies, Movie_model

router = APIRouter(prefix="/movie", tags=["movie"])

@router.post("/")
def get_movie(filter: Annotated[Movie_model, Query()]):
    filters = [col[0] for col in filter if col[1]]
    whr = []
    if "id" in filters: whr.append(Movies.id == filter.id)
    if "title" in filters: whr.append(Movies.title == filter.title)
    if "description" in filters: whr.append(Movies.description == filter.description)
    if "release" in filters: whr.append(Movies.release == filter.release)
    if "genre" in filters: whr.append(Movies.genre == filter.genre)
    with session_maker() as session:
        return session.scalars(select(Movies).where(*whr)).all()
