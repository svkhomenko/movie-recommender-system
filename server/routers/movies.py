from fastapi import APIRouter, Response, Query, status, HTTPException
from sqlmodel import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import InstrumentedAttribute
from typing import Annotated, cast
from dependencies.session import SessionDep
from dependencies.current_user import (
    CurrentUserForPersonalListsDep,
    OptionalCurrentUserDep,
)
from models.movie import (
    Movie,
    MoviePublic,
    OneMoviePublic,
    MoviePublicFilterSearchParams,
    MoviePublicResultType,
)
from models.movie_crew import MovieCrew, MovieCrewRoleEnum, CrewWithoutMovies
from services import movie as MovieService

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get(
    "/",
    response_model=list[MoviePublic],
    responses={401: {"description": "The access token is invalid or has expired"}},
)
async def get_movies(
    query: Annotated[MoviePublicFilterSearchParams, Query()],
    session: SessionDep,
    response: Response,
    cur_user: CurrentUserForPersonalListsDep,
):
    where = MovieService.get_where_options(query, cur_user)
    order_by = MovieService.get_order_by_options(query)

    GenresAttr = cast(InstrumentedAttribute, Movie.genres)

    subquery_ids = (
        select(Movie.id).select_from(Movie).join(GenresAttr).where(*where).distinct()
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

    if query.result_type == MoviePublicResultType.WATCH_LATER and cur_user:
        return MovieService.get_watch_later_movies(
            session, order_by, query, subquery_ids, cur_user
        )

    if query.result_type == MoviePublicResultType.WATCHED and cur_user:
        return MovieService.get_watched_movies(
            session, order_by, query, subquery_ids, cur_user
        )

    movies = session.exec(
        select(Movie)
        .join(GenresAttr)
        .where(*where)
        .order_by(*order_by)
        .limit(query.limit)
        .offset(query.offset)
        .distinct()
    ).all()

    return movies


@router.get(
    "/{id}",
    response_model=OneMoviePublic,
    responses={
        404: {"description": "No movie found"},
    },
)
def get_movie_by_id(id: int, session: SessionDep, cur_user: OptionalCurrentUserDep):
    MovieCrewAttr = cast(InstrumentedAttribute, Movie.movie_crew)
    CrewAttr = cast(InstrumentedAttribute, MovieCrew.crew)

    subqueries = MovieService.get_subquery_for_movie_by_id(cur_user)

    result = session.exec(
        select(Movie, *subqueries)
        .where(Movie.id == id)
        .options(selectinload(MovieCrewAttr).selectinload(CrewAttr))
        .limit(1)
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movie found",
        )

    MovieService.add_viewing_history(session, cur_user, id)

    movie, user_rating, watch_later, watched = result

    casts_public = []
    directors_public = []

    for mc in movie.movie_crew:
        if mc.id and movie.id:
            crew_data = CrewWithoutMovies(
                id=mc.id,
                movie_id=movie.id,
                crew_id=mc.crew_id,
                full_name=mc.crew.full_name,
                role=mc.role,
            )

        if mc.role == MovieCrewRoleEnum.CAST:
            casts_public.append(crew_data)
        elif mc.role == MovieCrewRoleEnum.DIRECTOR:
            directors_public.append(crew_data)

    movie_public_data = movie.model_dump()

    movie_public_data["rating"] = user_rating
    movie_public_data["watch_later"] = bool(watch_later)
    movie_public_data["watched"] = bool(watched)
    movie_public_data["genres"] = movie.genres
    movie_public_data["collections"] = movie.collections
    movie_public_data["casts"] = casts_public
    movie_public_data["directors"] = directors_public

    return OneMoviePublic(**movie_public_data)
