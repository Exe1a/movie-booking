from sqlalchemy import create_engine
from dotenv import dotenv_values
from fastapi import APIRouter
from models import Base

router = APIRouter(prefix="/db")

engine = create_engine(dotenv_values(".env").get("DATABASE_URL"))

@router.post("/reset")
def db_reset():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return {"status": "Database was reset."}