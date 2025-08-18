from sqlmodel import Field, SQLModel, Column, Relationship, Enum
from typing import TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from .movie import Movie
    from .crew import Crew


class MovieCrewRoleEnum(enum.Enum):
    CAST = "cast"
    DIRECTOR = "director"


# id
# movie_id
# crew_id
# role


class MovieCrew(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movie.id", ondelete="CASCADE")
    crew_id: int = Field(foreign_key="crew.id", ondelete="CASCADE")
    role: MovieCrewRoleEnum = Field(
        sa_column=Column(Enum(MovieCrewRoleEnum)), default=MovieCrewRoleEnum.CAST
    )

    movie: "Movie" = Relationship(back_populates="movie_crew")
    crew: "Crew" = Relationship(back_populates="movie_crew")
