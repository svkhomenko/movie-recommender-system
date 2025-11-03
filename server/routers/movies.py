from fastapi import APIRouter, Response, Query
from sqlmodel import select, func
from typing import Annotated
from dependencies.session import SessionDep
from dependencies.current_user import CurrentUserForPersonalListsDep
from models.movie import (
    Movie,
    MoviePublic,
    MoviePublicFilterSearchParams,
    MoviePublicResultType,
)
from services import movie as MovieService

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=list[MoviePublic])
async def get_movies(
    query: Annotated[MoviePublicFilterSearchParams, Query()],
    session: SessionDep,
    response: Response,
    cur_user: CurrentUserForPersonalListsDep,
):
    where = MovieService.get_where_options(query, cur_user)
    order_by = MovieService.get_order_by_options(query)

    subquery_ids = (
        select(Movie.id)
        .select_from(Movie)
        .join(Movie.genres)  # type: ignore
        .where(*where)
        .distinct()
    ).subquery()
    count = session.exec(select(func.count()).select_from(subquery_ids)).one()
    response.headers["X-Total-Count"] = str(count)

    if query.result_type == MoviePublicResultType.POPULAR_NOW:
        return MovieService.get_popular_now_movies(
            session, order_by, query, subquery_ids
        )

    if query.result_type == MoviePublicResultType.CONTINUE_WATCHING and cur_user:
        return MovieService.get_continue_watching_movies(
            session, order_by, query, subquery_ids, cur_user
        )

    movies = session.exec(
        select(Movie)
        .join(Movie.genres)  # type: ignore
        .where(*where)
        .order_by(*order_by)
        .limit(query.limit)
        .offset(query.offset)
        .distinct()
    ).all()

    return movies
