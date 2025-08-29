from sqlmodel import Field, SQLModel, Column, Relationship, TIMESTAMP, text
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .movie import Movie

# user_id
# movie_id
# created_at


class WatchLater(SQLModel, table=True):
    __tablename__: str = "watch_later"

    user_id: int | None = Field(
        default=None, foreign_key="user.id", primary_key=True, ondelete="CASCADE"
    )
    movie_id: int | None = Field(
        default=None, foreign_key="movie.id", primary_key=True, ondelete="CASCADE"
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )

    user: "User" = Relationship(back_populates="watch_later")
    movie: "Movie" = Relationship(back_populates="watch_later")
