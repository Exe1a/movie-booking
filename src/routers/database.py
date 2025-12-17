from fastapi import APIRouter
from src.database import engine
from src.models import Base

router = APIRouter(prefix="/db", tags=["database"])

@router.post("/reset")
def db_reset():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return {"status": "Database was reset."}