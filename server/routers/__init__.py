from fastapi import APIRouter
from . import auth, profile, movies, ratings

root_router = APIRouter()

root_router.include_router(auth.router)
root_router.include_router(profile.router)
root_router.include_router(movies.router)
root_router.include_router(ratings.router)
