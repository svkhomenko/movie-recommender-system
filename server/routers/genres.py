from fastapi import APIRouter
from sqlmodel import select
from dependencies.session import SessionDep
from models.genre import Genre, GenreWithoutMovies

router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("/", response_model=list[GenreWithoutMovies])
def get_genres(session: SessionDep):
    genres = session.exec(select(Genre)).all()
    return genres
