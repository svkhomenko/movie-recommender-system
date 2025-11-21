import uvicorn
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from exception_handler import register_exception_handlers
from sqladmin import Admin
from database import engine
from admin import auth
from admin.models import user, genre, collection, crew, movie, movie_crew
import recommender.recommender

load_dotenv()

from routers import root_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CLIENT_URL") or "http://localhost"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "Set-Cookie"],
    expose_headers=["X-Total-Count"],
)

register_exception_handlers(app)

app.include_router(root_router)

admin = Admin(app, engine, authentication_backend=auth.authentication_backend)
admin.add_view(user.UserAdmin)
admin.add_view(genre.GenreAdmin)
admin.add_view(collection.CollectionAdmin)
admin.add_view(crew.CrewAdmin)
admin.add_view(movie.MovieAdmin)
admin.add_view(movie_crew.MovieCrewAdmin)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=(os.getenv("SERVER_HOST") or "localhost"),
        port=int(os.getenv("SERVER_PORT") or 8000),
    )
