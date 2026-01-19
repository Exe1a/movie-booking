from fastapi import APIRouter, Query
from sqlalchemy import select
from typing import Annotated
from src.database import session_maker
from src.models.database import Users
from src.models.pydantic_models import User_form

router = APIRouter(prefix="/user",tags=["user"])

@router.post("/info")
def get_info(login: str):
    with session_maker() as session:
        return session.scalar(select(Users).where(Users.login == login))

@router.post("/registration")
def registration(user: Annotated[User_form, Query()]):
    new_user = Users(login = user.login,
                     password = user.password)
    with session_maker() as session:
        session.add(new_user)
        session.commit()
    return {"result": "user was added"}

@router.patch("/change_password")
def change_password(id:int, new_password: str):
    with session_maker() as session:
        user = session.get(Users, id)
        user.password = new_password
        session.commit()
    return {"result": "password was changed"}

@router.delete("")
def delete_user(id: int):
    with session_maker() as session:
        session.delete(session.get(Users, id))
        session.commit()
    return {"result": "user was deleted"}