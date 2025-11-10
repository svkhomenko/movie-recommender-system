from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .movie import Movie

# user_id
# movie_id
# rating


class Rating(SQLModel, table=True):
    user_id: int | None = Field(
        default=None, foreign_key="user.id", primary_key=True, ondelete="CASCADE"
    )
    movie_id: int | None = Field(
        default=None,
        foreign_key="movie.id",
        primary_key=True,
        ondelete="CASCADE",
        index=True,
    )
    rating: int

    user: "User" = Relationship(back_populates="ratings")
    movie: "Movie" = Relationship(back_populates="ratings")


class RatingCreate(SQLModel):
    rating: int = Field(ge=1, le=10)
