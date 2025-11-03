from sqlmodel import Session, select, func, or_, desc, col, and_
from sqlalchemy.sql import Subquery
from sqlalchemy.orm import aliased
from datetime import date, datetime, timedelta
from typing import Any
from models.movie import Movie, MoviePublicFilterSearchParams, MoviePublicResultType
from models.viewing_history import ViewingHistory
from models.genre import Genre
from models.user import User
from models.movie_collection import MovieCollection
from models.watched import Watched


def get_where_options(
    params: MoviePublicFilterSearchParams, cur_user: User | None
) -> list[Any]:
    where = []

    if params.q:
        search_term = f"%{params.q}%"
        where.append(
            or_(
                col(Movie.title).ilike(search_term),
                col(Movie.overview).ilike(search_term),
                col(Movie.keywords).ilike(search_term),
            )
        )

    if params.year_min:
        where.append(Movie.release_date >= date(params.year_min, 1, 1))
    if params.year_max:
        where.append(Movie.release_date <= date(params.year_max, 12, 31))

    if params.genre_ids:
        where.append(col(Genre.id).in_(params.genre_ids))

    if params.result_type == MoviePublicResultType.CONTINUE_WATCHING:
        if cur_user:
            watched_collection_ids_subquery = (
                select(MovieCollection.collection_id)
                .join(Watched, col(Watched.movie_id) == MovieCollection.movie_id)
                .where(Watched.user_id == cur_user.id)
                .distinct()
                .subquery()
            )

            where.append(
                col(Movie.id).in_(
                    select(MovieCollection.movie_id).where(
                        col(MovieCollection.collection_id).in_(
                            select(watched_collection_ids_subquery.c.collection_id)
                        )
                    )
                )
            )

            watched_movie_ids_subquery = (
                select(Watched.movie_id)
                .where(Watched.user_id == cur_user.id)
                .subquery()
            )

            where.append(
                col(Movie.id).not_in(select(watched_movie_ids_subquery.c.movie_id))
            )

    return where


def get_order_by_options(params: MoviePublicFilterSearchParams) -> list[Any]:
    if params.result_type == MoviePublicResultType.NEW:
        return [desc("release_date"), desc("vote_count"), desc("vote_average")]

    return [desc("vote_count"), desc("vote_average")]


def get_popular_now_movies(
    session: Session,
    order_by: list[Any],
    query: MoviePublicFilterSearchParams,
    subquery_ids: Subquery,
):
    view_count = func.count(col(ViewingHistory.id)).label("view_count")
    time_cutoff = datetime.now() - timedelta(days=30)

    results = session.exec(
        select(Movie, view_count)
        .where(col(Movie.id).in_(select(subquery_ids.c.id)))
        .outerjoin(
            ViewingHistory,
            and_(
                ViewingHistory.movie_id == Movie.id,
                col(ViewingHistory.created_at) >= time_cutoff,
            ),
        )
        .group_by(col(Movie.id))
        .order_by(desc(view_count), *order_by)
        .limit(query.limit)
        .offset(query.offset)
        .distinct()
    ).all()

    return [movie for movie, _ in results]


def get_continue_watching_movies(
    session: Session,
    order_by: list[Any],
    query: MoviePublicFilterSearchParams,
    subquery_ids: Subquery,
    cur_user: User,
):
    OtherMovieCollection = aliased(MovieCollection, name="other_movies_in_collection")

    last_watched_per_movie = (
        select(Watched.movie_id, func.max(Watched.created_at).label("latest_watch"))
        .where(Watched.user_id == cur_user.id)
        .group_by(col(Watched.movie_id))
    ).cte("last_watched_per_movie")

    max_collection_watched_date = func.max(last_watched_per_movie.c.latest_watch).label(
        "last_watched_date"
    )

    results = session.exec(
        select(Movie, max_collection_watched_date)
        .where(col(Movie.id).in_(select(subquery_ids.c.id)))
        .join(MovieCollection, col(MovieCollection.movie_id) == Movie.id)
        .join(
            OtherMovieCollection,
            col(OtherMovieCollection.collection_id) == MovieCollection.collection_id,
        )
        .outerjoin(
            last_watched_per_movie,
            last_watched_per_movie.c.movie_id == OtherMovieCollection.movie_id,
        )
        .group_by(col(Movie.id))
        .order_by(desc(max_collection_watched_date), *order_by)
        .limit(query.limit)
        .offset(query.offset)
    ).all()

    return [movie for movie, _ in results]
