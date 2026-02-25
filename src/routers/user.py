from fastapi import APIRouter, Query, Response, Cookie, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated
from src.database.orm import get_session
from src.database.models import Users
from src.schemas.user import UserForm
from src.auth import generate_token, admin_check, get_user_id, hash_password, check_password

router = APIRouter(prefix="/user",
                   tags=["user"])

@router.post(path="/registration")
def registration(user: Annotated[UserForm, Query()],
                 response: Response,
                 session: Session = Depends(get_session)):
    if session.scalar(select(Users.login).where(Users.login == user.login)):
        raise HTTPException(409, "Login already exist")
    hash_pd = hash_password(user.password)
    new_user = Users(login = user.login,
                     password = hash_pd)
    session.add(new_user)
    session.commit()
    user_id = session.scalar(select(Users.id).where(Users.login == user.login))
    response.set_cookie("token", generate_token(user_id))
    return {"result": "user was registered"}

@router.post(path="/login")
def login_user(user_data: Annotated[UserForm, Query()],
               response: Response,
               session: Session = Depends(get_session)):
    error = {"error": "login or password incorrect"}
    user_from_db = session.scalar(select(Users).where(Users.login == user_data.login))
    if user_from_db.login == "":
        return error
    if check_password(user_data.password, user_from_db.password):
        response.set_cookie("token", generate_token(user_from_db.id))
        return {"result": "Successful login"}
    return error

@router.patch(path="/change_password/{user_id}")
def change_password(user_id: int,
                    new_password: str,
                    token: Annotated[str, Cookie()],
                    session: Session = Depends(get_session)):
    if get_user_id(token) != user_id:
        return {"error": "You can change password only your account"}
    user = session.get(Users, user_id)
    user.password = hash_password(new_password)
    session.commit()
    return {"result": "password was changed"}

@router.delete(path="/{user_id}")
def delete_user(user_id: int,
                token: Annotated[str, Cookie()],
                session: Session = Depends(get_session)):
    admin_check(token)
    session.delete(session.get(Users, user_id))
    session.commit()
    return {"result": "user was deleted"}