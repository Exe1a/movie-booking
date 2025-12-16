from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

engine = create_engine(dotenv_values(".env").get("DATABASE_URL"),
                       echo=True)

session_maker = sessionmaker(engine)