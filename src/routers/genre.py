from fastapi import APIRouter
from sqlalchemy import select
from src.models import Movies_Genres
from src.database import session_maker

router = APIRouter(prefix="/genre", tags=["genre"])

@router.get("")
def list_genres():
    with session_maker() as session:
        return session.scalars(select(Movies_Genres)).all()

@router.post("")
def add_genre(new_genre: str):
    with session_maker() as session:
        genre = Movies_Genres(genre=new_genre)
        session.add(genre)
        session.commit()
    return {"result":"genre was added"}

@router.patch("")
def edit_genre(genre_id: int, genre_new_name: str):
    with session_maker() as session:
        genre_obj = session.scalar(select(Movies_Genres).where(Movies_Genres.id == genre_id))
        genre_obj.genre = genre_new_name
        session.commit()
    return {"result":"genre was renamed"}

@router.delete("")
def delete_genre(genre_id: int):
    with session_maker() as session:
        genre_to_delete = session.get(Movies_Genres, genre_id)
        session.delete(genre_to_delete)
        session.commit()
    return {"result":"genre with movies was "}