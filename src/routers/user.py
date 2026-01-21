from fastapi import APIRouter, Query, Response, Cookie, Depends
from sqlalchemy import select
from typing import Annotated
from src.database import get_session
from src.models.database import Users
from src.models.pydantic_models import User_form
from src.utils import generate_token, admin_check, get_user_id

router = APIRouter(prefix="/user",tags=["user"])

@router.post("/info/{login}")
def get_info(login: str,
             token: Annotated[str, Cookie()],
             session = Depends(get_session)):
    Depends(admin_check(token))
    return session.scalar(select(Users).where(Users.login == login))

@router.post("/registration")
def registration(user: Annotated[User_form, Query()],
                 session = Depends(get_session)):
    new_user = Users(login = user.login,
                     password = user.password)
    session.add(new_user)
    session.commit()
    return {"result": "user was added"}

@router.post("/login")
def login_user(login: str,
               password: str,
               response: Response,
               session = Depends(get_session)):
    error = {"error": "login or password incorrect"}
    user = session.scalar(select(Users).where(Users.login == login))
    if user.password == password:
        response.set_cookie("token", generate_token(user.id))
        return {"result": "Successful login"}
    else:
        return error

@router.patch("/change_password/{user_id}")
def change_password(user_id: int,
                    new_password: str,
                    token: Annotated[str, Cookie()],
                    session = Depends(get_session)):
    if get_user_id(token) != user_id: return {"error": "You can change password only your account"}
    user = session.get(Users, user_id)
    user.password = new_password
    session.commit()
    return {"result": "password was changed"}

@router.delete("/{user_id}")
def delete_user(user_id: int,
                token: Annotated[str, Cookie()],
                session = Depends(get_session)):
    Depends(admin_check(token))
    session.delete(session.get(Users, user_id))
    session.commit()
    return {"result": "user was deleted"}