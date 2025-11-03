from fastapi import APIRouter, status, Response
from dependencies.session import SessionDep
from dependencies.current_user import CurrentUserDep
from models.rating import Rating, RatingCreate
from services import movie as MovieService
from services import rating as RatingService

router = APIRouter(prefix="/movies", tags=["movies"])


@router.post(
    "/{movie_id}/rating",
    response_model=Rating,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"description": "The access token is invalid or has expired"},
        404: {"description": "No movie found"},
    },
    tags=["ratings"],
)
def create_rating(
    movie_id: int,
    session: SessionDep,
    cur_user: CurrentUserDep,
    rating_data: RatingCreate,
):
    MovieService.find_one_or_throw(session, movie_id)
    return RatingService.create_or_update(
        session, movie_id, cur_user, rating_data.rating
    )


@router.delete(
    "/{movie_id}/rating",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "The access token is invalid or has expired"},
        404: {"description": "No movie found"},
    },
    tags=["ratings"],
)
async def delete_rating(
    movie_id: int,
    session: SessionDep,
    cur_user: CurrentUserDep,
    response: Response,
):
    MovieService.find_one_or_throw(session, movie_id)
    RatingService.delete(session, movie_id, cur_user)

    response.status_code = status.HTTP_204_NO_CONTENT
    return response
