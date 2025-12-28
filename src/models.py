from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, ForeignKey, CheckConstraint
from pydantic import BaseModel
from datetime import date, datetime

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    login: Mapped[str] = mapped_column(String(32), nullable=False)
    password: Mapped[str] = mapped_column(String(32), nullable=False)
    admin: Mapped[bool] = mapped_column(server_default="False")

class Movies(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str]
    release: Mapped[date]
    genre_id: Mapped[int] = mapped_column(ForeignKey("movies_genres.id", ondelete="CASCADE"))

class Movies_Genres(Base):
    __tablename__ = "movies_genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    genre: Mapped[str] = mapped_column(String(32), unique=True)

class Showtimes(Base):
    __tablename__ = "showtimes"
    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[str] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"))
    time: Mapped[datetime]
    seats: Mapped[int]
    reserved: Mapped[int] = mapped_column(server_default='0')

    CheckConstraint("seats >= reserved")

class Movie_model(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    release: date | None = None
    genre_id: int | None = None

    def get_fields(self) -> list:
        fields = []
        if self.id: fields.append("id")
        if self.title: fields.append("title")
        if self.description: fields.append("description")
        if self.release: fields.append("release")
        if self.genre_id: fields.append("genre_id")
        return fields