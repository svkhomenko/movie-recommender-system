from sqlmodel import Field, SQLModel

# movie_id
# collection_id


class MovieCollection(SQLModel, table=True):
    __tablename__: str = "movie_collection"

    movie_id: int | None = Field(
        default=None, foreign_key="movie.id", primary_key=True, ondelete="CASCADE"
    )
    collection_id: int | None = Field(
        default=None, foreign_key="collection.id", primary_key=True, ondelete="CASCADE"
    )
