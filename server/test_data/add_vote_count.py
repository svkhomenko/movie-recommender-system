import pandas as pd
from sqlmodel import Session
from database import engine
import models
from test_data.fill_db import get_path


def add_vote_count():
    movies_df = pd.read_json(
        get_path("movies.json"), orient="records", convert_dates=["release_date"]
    )

    with Session(engine) as session:
        for row in movies_df.itertuples():
            movie = session.get(models.Movie, row.id)

            if movie:
                movie.vote_count = int(str(row.vote_count))
                session.add(movie)
                session.commit()


if __name__ == "__main__":
    add_vote_count()
    print("Successfully added vote_count")
