from fastapi import FastAPI
import src.routers.database as db
import src.routers.movie as movie

app = FastAPI()

app.include_router(db.router)
app.include_router(movie.router)