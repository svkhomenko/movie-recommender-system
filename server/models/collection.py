from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING
from models.movie_collection import MovieCollection

if TYPE_CHECKING:
    from .movie import Movie


# id
# name


class Collection(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()

    movies: list["Movie"] = Relationship(
        back_populates="collections", link_model=MovieCollection
    )


class CollectionWithoutMovies(SQLModel):
    id: int
    name: str
