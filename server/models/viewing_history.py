from sqlmodel import Field, SQLModel, Column, Relationship, TIMESTAMP, text
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .movie import Movie

# id
# user_id
# movie_id
# created_at


class ViewingHistory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE")
    movie_id: int = Field(foreign_key="movie.id", ondelete="CASCADE")
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )

    user: "User" = Relationship(back_populates="viewing_history")
    movie: "Movie" = Relationship(back_populates="viewing_history")
