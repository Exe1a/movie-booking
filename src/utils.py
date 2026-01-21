from jwt import decode, encode
from bcrypt import hashpw, gensalt, checkpw
from dotenv import dotenv_values
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.database import Users
from src.database import engine
from fastapi import HTTPException

secret_key = str(dotenv_values(".env").get("SECRET_JWT_KEY"))
algorithm = "HS256"

def generate_token(user_id) -> str:
    return encode(payload={"user_id": user_id},
                  key=secret_key,
                  algorithm=algorithm)

def get_user_id(token: str):
    decoded_token = decode(jwt=token,
                           key=secret_key,
                           algorithms=algorithm)
    return decoded_token.get("user_id")

def admin_check(token: str | bytes) -> None:
    user_id = get_user_id(token)
    with Session(engine) as session:
        admin = session.scalar(select(Users.admin).where(Users.id == user_id))
    if not admin:
        raise HTTPException(403, "You are not admin")

def hash_password(password: str) -> str:
    return (hashpw(password.encode(), gensalt())).decode()

def check_password(password: str,
                   hashed_password: str) -> bool:
    return checkpw(password.encode(), hashed_password.encode())