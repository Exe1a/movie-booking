from fastapi import FastAPI
import src.routers.database as db
import src.routers.movie as movie
import src.routers.genre as genre
import src.routers.showtimes as showtimes

app = FastAPI()

app.include_router(db.router)
app.include_router(movie.router)
app.include_router(genre.router)
app.include_router(showtimes.router)