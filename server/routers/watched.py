from fastapi import APIRouter, status, Response
from dependencies.session import SessionDep
from dependencies.current_user import CurrentUserDep
from models.watched import Watched
from services import movie as MovieService
from services import watched as WatchedService

router = APIRouter(prefix="/movies", tags=["movies"])


@router.post(
    "/{movie_id}/watched",
    response_model=Watched,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"description": "The access token is invalid or has expired"},
        404: {"description": "No movie found"},
    },
    tags=["watched"],
)
def create_watched(movie_id: int, session: SessionDep, cur_user: CurrentUserDep):
    MovieService.find_one_or_throw(session, movie_id)
    return WatchedService.create_or_update(session, movie_id, cur_user)


@router.delete(
    "/{movie_id}/watched",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "The access token is invalid or has expired"},
        404: {"description": "No movie found"},
    },
    tags=["watched"],
)
def delete_watched(
    movie_id: int,
    session: SessionDep,
    cur_user: CurrentUserDep,
    response: Response,
):
    MovieService.find_one_or_throw(session, movie_id)
    WatchedService.delete(session, movie_id, cur_user)

    response.status_code = status.HTTP_204_NO_CONTENT
    return response
