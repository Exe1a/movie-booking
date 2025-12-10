from fastapi import FastAPI
import database as db

app = FastAPI()

app.add_api_route(db.router)