from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database import session_maker
from src.models import Movie, Movie_model

router = APIRouter(prefix="/movie")

@router.post("/{id}")
def get_movie(filter: Movie_model):
    try:
        with session_maker() as session:
            return session.scalars(
                select(Movie).where(
                    Movie.id == filter.id,
                    Movie.name == filter.name,
                    Movie.description == filter.description,
                    Movie.release == filter.realese,
                    Movie.genre == filter.genre
                )
            )
    except Exception as e:
        raise HTTPException(409, "Some problem with filter")