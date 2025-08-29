from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING
from models.movie_genre import MovieGenre

if TYPE_CHECKING:
    from .movie import Movie


# id
# name


class Genre(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()

    movies: list["Movie"] = Relationship(back_populates="genres", link_model=MovieGenre)
