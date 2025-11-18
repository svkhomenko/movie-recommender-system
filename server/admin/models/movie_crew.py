from sqladmin import ModelView
from starlette.requests import Request
from sqlalchemy.orm import selectinload
from models.movie_crew import MovieCrew


class MovieCrewAdmin(ModelView, model=MovieCrew):
    name = "Movie Crew Link"
    name_plural = "Movie Crew Links"

    column_list = ["id", "movie", "crew", "role"]

    column_searchable_list = ["movie_id", "crew_id"]
    column_sortable_list = ["id", "movie_id", "crew_id", "role"]

    form_create_rules = ["movie", "crew", "role"]

    form_edit_rules = form_create_rules

    column_details_list = ["id", "movie", "crew", "role"]

    form_ajax_refs = {
        "movie": {
            "fields": (
                "id",
                "title",
            ),
            "order_by": "id",
        },
        "crew": {
            "fields": (
                "id",
                "full_name",
            ),
            "order_by": "id",
        },
    }

    def is_visible(self, request: Request) -> bool:
        return request.session.get("admin_jwt") is not None

    def is_accessible(self, request: Request) -> bool:
        return request.session.get("admin_jwt") is not None
