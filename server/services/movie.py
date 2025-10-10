from sqlmodel import Session, select, func, or_, desc
from sqlalchemy.sql import Subquery
from datetime import date, datetime, timedelta
from typing import Any
from models.movie import Movie, MoviePublicFilterSearchParams, MoviePublicResultType
from models.viewing_history import ViewingHistory
from models.genre import Genre


def get_where_options(params: MoviePublicFilterSearchParams) -> list[Any]:
    where = []

    if params.q:
        search_term = f"%{params.q}%"
        where.append(
            or_(
                Movie.title.ilike(search_term),  # type: ignore
                Movie.overview.ilike(search_term),  # type: ignore
                Movie.keywords.ilike(search_term),  # type: ignore
            )
        )

    if params.year_min:
        where.append(Movie.release_date >= date(params.year_min, 1, 1))
    if params.year_max:
        where.append(Movie.release_date <= date(params.year_max, 12, 31))

    if params.genre_ids:
        where.append(Genre.id.in_(params.genre_ids))  # type: ignore

    if params.result_type == MoviePublicResultType.POPULAR_NOW:
        time_cutoff = datetime.now() - timedelta(days=30)
        where.append(
            or_(
                ViewingHistory.created_at >= time_cutoff,  # type: ignore
                ViewingHistory.created_at.is_(None),  # type: ignore
            )
        )

    return where


def get_order_by_options(params: MoviePublicFilterSearchParams) -> list[Any]:
    if params.result_type == MoviePublicResultType.NEW:
        return [desc("release_date"), desc("vote_count"), desc("vote_average")]

    return [desc("vote_count"), desc("vote_average")]


def get_popular_now_movies(
    session: Session,
    where: list[Any],
    order_by: list[Any],
    query: MoviePublicFilterSearchParams,
    subquery_ids: Subquery,
):
    view_count = func.count(ViewingHistory.id).label("view_count")  # type: ignore

    results = session.exec(
        select(Movie, view_count)
        .where(Movie.id.in_(subquery_ids))  # type: ignore
        .outerjoin(Movie.viewing_history)  # type: ignore
        .where(*where)
        .group_by(Movie.id)  # type: ignore
        .order_by(desc(view_count), *order_by)
        .limit(query.limit)
        .offset(query.offset)
        .distinct()
    ).all()

    return [movie for movie, _ in results]
