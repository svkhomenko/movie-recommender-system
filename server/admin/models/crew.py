from sqladmin import ModelView
from database import engine
from sqlmodel import Session, select
from starlette.requests import Request
from models.crew import Crew
from ..formatters import _format_movie_crew_details_view


class CrewAdmin(ModelView, model=Crew):
    name = "Crew"
    name_plural = "Crew"

    column_list = ["id", "full_name"]
    column_details_list = ["id", "full_name", "movie_crew"]
    form_excluded_columns = ["movie_crew"]

    column_searchable_list = ["full_name"]
    column_sortable_list = ["id", "full_name"]

    column_formatters_detail = {"movie_crew": _format_movie_crew_details_view}

    async def on_model_change(self, data, model, is_created, request):
        with Session(engine) as session:
            crew = session.exec(
                select(Crew)
                .where(Crew.full_name == data["full_name"], Crew.id != model.id)
                .limit(1)
            ).first()

            if crew:
                raise Exception("This crew member already exists")

    def is_visible(self, request: Request) -> bool:
        return request.session.get("admin_jwt") is not None

    def is_accessible(self, request: Request) -> bool:
        return request.session.get("admin_jwt") is not None


# from sqladmin import ModelView
# from database import engine
# from sqlmodel import Session, select
# from starlette.requests import Request
# from models.crew import Crew
# from ..formatters import _format_movie_crew_details_view


# class CrewAdmin(ModelView, model=Crew):
#     name = "Crew"
#     name_plural = "Crew"

#     column_list = ["id", "full_name"]
#     column_details_list = ["id", "full_name", "movie_crew"]
#     form_excluded_columns = ["movie_crew"]

#     column_searchable_list = ["full_name"]
#     column_sortable_list = ["id", "full_name"]

#     column_formatters_detail = {"movie_crew": _format_movie_crew_details_view}

#     async def on_model_change(self, data, model, is_created, request):
#         with Session(engine) as session:
#             crew = session.exec(
#                 select(Crew)
#                 .where(Crew.full_name == data["full_name"], Crew.id != model.id)
#                 .limit(1)
#             ).first()

#             if crew:
#                 raise Exception("This crew member already exists")

#     def is_visible(self, request: Request) -> bool:
#         return request.session.get("admin_jwt") is not None

#     def is_accessible(self, request: Request) -> bool:
#         return request.session.get("admin_jwt") is not None
