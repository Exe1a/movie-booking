from sqlalchemy import create_engine
from dotenv import dotenv_values

engine = create_engine(dotenv_values(".env")["DATABASE_URL"])