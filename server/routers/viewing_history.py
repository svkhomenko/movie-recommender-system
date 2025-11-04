from fastapi import APIRouter, status, Response
from dependencies.session import SessionDep
from dependencies.current_user import CurrentUserDep
from services import movie as MovieService
from services import viewing_history as ViewingHistoryService

router = APIRouter(prefix="/movies", tags=["movies"])


@router.delete(
    "/{movie_id}/viewing_history",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "The access token is invalid or has expired"},
        404: {"description": "No movie found"},
    },
    tags=["viewing_history"],
)
def delete_viewing_history(
    movie_id: int,
    session: SessionDep,
    cur_user: CurrentUserDep,
    response: Response,
):
    MovieService.find_one_or_throw(session, movie_id)
    ViewingHistoryService.delete_all(session, movie_id, cur_user)

    response.status_code = status.HTTP_204_NO_CONTENT
    return response
