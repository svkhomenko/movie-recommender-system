from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .movie_crew import MovieCrew


# id
# full_name


class Crew(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str = Field()

    movie_crew: list["MovieCrew"] = Relationship(
        back_populates="crew", cascade_delete=True
    )
