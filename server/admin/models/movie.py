from sqladmin import ModelView
from starlette.requests import Request
from models.movie import Movie
from ..formatters import (
    _format_genres_collections_details_view,
    _format_crew_movie_details_view,
)


class MovieAdmin(ModelView, model=Movie):
    name = "Movie"
    name_plural = "Movies"

    column_list = [
        "id",
        "title",
        "release_date",
        "vote_average",
        "vote_count",
        "genres",
        "collections",
    ]
    column_searchable_list = ["title", "overview"]
    column_sortable_list = ["id", "title", "release_date", "vote_average"]

    form_excluded_columns = [
        "viewing_history",
        "ratings",
        "watch_later",
        "watched",
    ]

    form_create_rules = [
        "id",
        "title",
        "overview",
        "keywords",
        "release_date",
        "poster_path",
        "vote_average",
        "vote_count",
        "genres",
        "collections",
    ]

    form_edit_rules = form_create_rules

    column_details_list = [
        "id",
        "title",
        "overview",
        "keywords",
        "release_date",
        "poster_path",
        "vote_average",
        "vote_count",
        "genres",
        "collections",
        "movie_crew",
    ]

    column_formatters_detail = {
        "genres": _format_genres_collections_details_view,
        "collections": _format_genres_collections_details_view,
        "movie_crew": _format_crew_movie_details_view,
    }

    def is_visible(self, request: Request) -> bool:
        return request.session.get("admin_jwt") is not None

    def is_accessible(self, request: Request) -> bool:
        return request.session.get("admin_jwt") is not None
