from sqladmin import ModelView
from database import engine
from sqlmodel import Session, select
from starlette.requests import Request
from models.genre import Genre
from ..formatters import _format_movies_details_view


class GenreAdmin(ModelView, model=Genre):
    name = "Genre"
    name_plural = "Genres"

    column_list = ["id", "name"]
    column_details_list = ["id", "name", "movies"]
    form_excluded_columns = ["movies"]

    column_searchable_list = ["name"]
    column_sortable_list = ["id", "name"]

    column_formatters_detail = {"movies": _format_movies_details_view}

    async def on_model_change(self, data, model, is_created, request):
        with Session(engine) as session:
            genre = session.exec(
                select(Genre)
                .where(Genre.name == data["name"], Genre.id != model.id)
                .limit(1)
            ).first()

            if genre:
                raise Exception("This genre already exists")

    def is_visible(self, request: Request) -> bool:
        return request.session.get("admin_jwt") is not None

    def is_accessible(self, request: Request) -> bool:
        return request.session.get("admin_jwt") is not None
