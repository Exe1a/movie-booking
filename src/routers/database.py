from fastapi import APIRouter, Depends, Cookie
from typing import Annotated
from src.database import engine
from src.models.database import Base
from src.utils import admin_check

router = APIRouter(prefix="/db", tags=["database"])

@router.post("/reset", summary="[WARNING] DELETE AND RECREATE ALL TABLES IN DATABASE")
def db_reset(token: Annotated[str, Cookie()]):
    Depends(admin_check(token))
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return {"status": "Database was reset."}