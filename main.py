from fastapi import FastAPI
import src.routers.database as db
import src.routers.movie as movie
import src.routers.genre as genre
import src.routers.showtimes as showtimes
import src.routers.reservation as reservation
import src.routers.user as user

app = FastAPI()

app.include_router(db.router)
app.include_router(movie.router)
app.include_router(genre.router)
app.include_router(showtimes.router)
app.include_router(reservation.router)
app.include_router(user.router)