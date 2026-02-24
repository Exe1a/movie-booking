from fastapi import APIRouter, HTTPException
from src.database.orm import engine, database_reset_key
from src.database.models import Base

router = APIRouter(prefix="/db",
                   tags=["database"])

@router.post(path="/reset",
             summary="[WARNING] DELETE AND RECREATE ALL TABLES IN DATABASE")
def db_reset(key: str):
    if database_reset_key != key:
        raise HTTPException(403, "Key is invalid")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return {"status": "Database was reset."}