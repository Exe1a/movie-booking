from sqlalchemy import create_engine
from dotenv import dotenv_values
from sqlalchemy.orm import Session

url = str(dotenv_values(".env").get("POSTGRESQL_URL"))
database_reset_key = str(dotenv_values(".env").get("DATABASE_RESET_KEY"))

engine = create_engine(url=url,
                       echo=True)

def get_session():
    with Session(engine) as session:
        yield session