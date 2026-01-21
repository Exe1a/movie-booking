from fastapi import APIRouter, Query, Response, Cookie, Depends, HTTPException
from sqlalchemy import select
from typing import Annotated
from src.database import get_session
from src.models.database import Users
from src.models.pydantic_models import User_form
from src.utils import generate_token, admin_check, get_user_id

router = APIRouter(prefix="/user",tags=["user"])

@router.post("/registration")
def registration(user: Annotated[User_form, Query()],
                 response: Response,
                 session = Depends(get_session)):
    if session.scalar(select(Users.login).where(Users.login == user.login)):
        raise HTTPException(409, "Login already exist")
    new_user = Users(login = user.login,
                     password = user.password)
    session.add(new_user)
    session.commit()
    user_id = session.scalar(select(Users.id).where(Users.login == user.login))
    response.set_cookie("token", generate_token(user_id))
    return {"result": "user was registered"}

@router.post("/login")
def login_user(user_data: Annotated[User_form, Query()],
               response: Response,
               session = Depends(get_session)):
    error = {"error": "login or password incorrect"}
    user = session.scalar(select(Users).where(Users.login == user_data.login))
    if user.login == "":
        return error
    if user.password == user.password:
        response.set_cookie("token", generate_token(user.id))
        return {"result": "Successful login"}
    return error

@router.patch("/change_password/{user_id}")
def change_password(user_id: int,
                    new_password: str,
                    token: Annotated[str, Cookie()],
                    session = Depends(get_session)):
    if get_user_id(token) != user_id:
        return {"error": "You can change password only your account"}
    user = session.get(Users, user_id)
    user.password = new_password
    session.commit()
    return {"result": "password was changed"}

@router.delete("/{user_id}")
def delete_user(user_id: int,
                token: Annotated[str, Cookie()],
                session = Depends(get_session)):
    admin_check(token)
    session.delete(session.get(Users, user_id))
    session.commit()
    return {"result": "user was deleted"}