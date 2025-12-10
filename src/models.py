from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    login: Mapped[str] = mapped_column(String(30), nullable=False)
    password: Mapped[str] = mapped_column(String(30), nullable=False)
    admin: Mapped[bool] = mapped_column(Boolean, default=False)

class Movie(Base):
    __tablename__ = "movie"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    release: Mapped[datetime] = mapped_column(DateTime())
    genre: Mapped[str] = mapped_column(ForeignKey("movie_genre.genre"))

class Movie_Genre(Base):
    __tablename__ = "movie_genre"
    genre: Mapped[str] = mapped_column(primary_key=True)