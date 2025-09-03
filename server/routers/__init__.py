from fastapi import APIRouter
from . import auth

root_router = APIRouter()

root_router.include_router(auth.router)
