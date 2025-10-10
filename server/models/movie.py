from sqlmodel import Field, SQLModel, Column, Relationship
from enum import Enum
from datetime import date
from sqlalchemy.dialects import mysql
from models.movie_genre import MovieGenre
from models.movie_collection import MovieCollection
from .genre import GenreWithoutMovies
from .collection import CollectionWithoutMovies
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
# vote_average
# vote_count


class Movie(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field()
    overview: str = Field(sa_column=Column(mysql.TEXT))
    keywords: str = Field(sa_column=Column(mysql.TEXT))
    release_date: date = Field()
    poster_path: str = Field()
    vote_average: float = Field(default=0.0)
    vote_count: int = Field(default=0)

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


class MoviePublic(SQLModel):
    id: int
    title: str
    overview: str
    keywords: str
    release_date: date
    poster_path: str
    vote_average: float
    vote_count: int

    genres: list["GenreWithoutMovies"] = []
    collections: list["CollectionWithoutMovies"] = []


class MoviePublicResultType(str, Enum):
    BEST_RATING = "best_rating"
    NEW = "new"
    POPULAR_NOW = "popular_now"


class MoviePublicFilterSearchParams(SQLModel):
    limit: int = Field(default=10, ge=0)
    offset: int = Field(default=0, ge=-1)
    q: str | None = None
    year_min: int | None = Field(default=None, ge=0)
    year_max: int | None = Field(default=None, ge=0)
    genre_ids: list[int] = []
    result_type: MoviePublicResultType = MoviePublicResultType.BEST_RATING


MoviePublic.model_rebuild()
