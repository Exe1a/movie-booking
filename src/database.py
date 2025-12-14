from sqlalchemy import create_engine
from dotenv import dotenv_values

engine = create_engine(dotenv_values(".env").get("DATABASE_URL"))