from fastapi import APIRouter
from . import (
    auth,
    profile,
    movies,
    ratings,
    watch_later,
    watched,
    viewing_history,
    genres,
)

root_router = APIRouter()

root_router.include_router(auth.router)
root_router.include_router(profile.router)
root_router.include_router(movies.router)
root_router.include_router(ratings.router)
root_router.include_router(watch_later.router)
root_router.include_router(watched.router)
root_router.include_router(viewing_history.router)
root_router.include_router(genres.router)
