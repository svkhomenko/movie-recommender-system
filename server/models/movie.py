from sqlmodel import Field, SQLModel, Column, Relationship
from datetime import date
from sqlalchemy.dialects import mysql
from models.movie_genre import MovieGenre
from models.movie_collection import MovieCollection
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .viewing_history import ViewingHistory
    from .rating import Rating
    from .watch_later import WatchLater
    from .watched import Watched
    from .movie_crew import MovieCrew
    from .genre import Genre
    from .collection import Collection


# id
# title
# overview
# keywords
# release_date
# poster_path


class Movie(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field()
    overview: str = Field(sa_column=Column(mysql.TEXT))
    keywords: str = Field(sa_column=Column(mysql.TEXT))
    release_date: date = Field()
    poster_path: str = Field()

    viewing_history: list["ViewingHistory"] = Relationship(
        back_populates="movie", cascade_delete=True
    )
    ratings: list["Rating"] = Relationship(back_populates="movie", cascade_delete=True)
    watch_later: list["WatchLater"] = Relationship(
        back_populates="movie", cascade_delete=True
    )
    watched: list["Watched"] = Relationship(back_populates="movie", cascade_delete=True)
    movie_crew: list["MovieCrew"] = Relationship(
        back_populates="movie", cascade_delete=True
    )
    genres: list["Genre"] = Relationship(back_populates="movies", link_model=MovieGenre)
    collections: list["Collection"] = Relationship(
        back_populates="movies", link_model=MovieCollection
    )
