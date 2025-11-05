from fastapi import APIRouter, status, Response
from dependencies.session import SessionDep
from dependencies.current_user import CurrentUserDep
from models.watch_later import WatchLater
from services import movie as MovieService
from services import watch_later as WatchLaterService

router = APIRouter(prefix="/movies", tags=["movies"])


@router.post(
    "/{movie_id}/watch_later",
    response_model=WatchLater,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"description": "The access token is invalid or has expired"},
        404: {"description": "No movie found"},
    },
    tags=["watch_later"],
)
def create_watch_later(movie_id: int, session: SessionDep, cur_user: CurrentUserDep):
    MovieService.find_one_or_throw(session, movie_id)
    return WatchLaterService.create_if_doesnt_exist(session, movie_id, cur_user)


@router.delete(
    "/{movie_id}/watch_later",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "The access token is invalid or has expired"},
        404: {"description": "No movie found"},
    },
    tags=["watch_later"],
)
def delete_watch_later(
    movie_id: int,
    session: SessionDep,
    cur_user: CurrentUserDep,
    response: Response,
):
    MovieService.find_one_or_throw(session, movie_id)
    WatchLaterService.delete(session, movie_id, cur_user)

    response.status_code = status.HTTP_204_NO_CONTENT
    return response
