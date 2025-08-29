from sqlmodel import Field, SQLModel

# movie_id
# genre_id


class MovieGenre(SQLModel, table=True):
    __tablename__: str = "movie_genre"

    movie_id: int | None = Field(
        default=None, foreign_key="movie.id", primary_key=True, ondelete="CASCADE"
    )
    genre_id: int | None = Field(
        default=None, foreign_key="genre.id", primary_key=True, ondelete="CASCADE"
    )
