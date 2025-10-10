import pandas as pd
from pathlib import Path
from sqlmodel import Session, select
from database import engine
import models
from typing import cast, Dict


def get_path(filename: str):
    return Path(__file__).parent / "data" / filename


def get_or_create(session: Session, model, **kwargs):
    instance = session.exec(select(model).filter_by(**kwargs)).first()

    if instance:
        return instance

    instance = model(**kwargs)
    session.add(instance)
    return instance


def fill_db_with_movies():
    movies_df = pd.read_json(
        get_path("movies.json"), orient="records", convert_dates=["release_date"]
    )

    with Session(engine) as session:
        for row in movies_df.itertuples():
            movie_data = {
                "id": row.id,
                "title": row.title,
                "overview": row.overview,
                "keywords": row.keywords,
                "poster_path": row.poster_path,
                "release_date": cast(pd.Timestamp, row.release_date).date(),
                "vote_average": row.vote_average,
            }
            movie = get_or_create(session, models.Movie, **movie_data)

            if isinstance(row.belongs_to_collection, dict):
                collection = get_or_create(
                    session, models.Collection, **row.belongs_to_collection
                )
                if movie not in collection.movies:
                    collection.movies.append(movie)
                    session.add(collection)

            if isinstance(row.genres, list):
                for genre_data in row.genres:
                    if isinstance(genre_data, dict):
                        genre = get_or_create(session, models.Genre, **genre_data)
                        if movie not in genre.movies:
                            genre.movies.append(movie)
                            session.add(genre)

            if isinstance(row.cast, list):
                for cast_member_data in row.cast:
                    if isinstance(cast_member_data, dict):
                        cast_member = get_or_create(
                            session,
                            models.Crew,
                            id=cast_member_data["id"],
                            full_name=cast_member_data["name"],
                        )
                        get_or_create(
                            session,
                            models.MovieCrew,
                            movie=movie,
                            crew=cast_member,
                            role=models.MovieCrewRoleEnum.CAST,
                        )

            if isinstance(row.crew, dict):
                director = get_or_create(
                    session,
                    models.Crew,
                    id=cast(Dict, row.crew)["id"],
                    full_name=cast(Dict, row.crew)["name"],
                )
                get_or_create(
                    session,
                    models.MovieCrew,
                    movie=movie,
                    crew=director,
                    role=models.MovieCrewRoleEnum.DIRECTOR,
                )

            session.commit()


def fill_db_with_ratings():
    ratings_df = pd.read_json(get_path("ratings.json"), orient="records")

    with Session(engine) as session:
        for row in ratings_df.itertuples():
            movie = session.get(models.Movie, row.movieId)
            if movie:
                user = get_or_create(
                    session,
                    models.User,
                    id=row.userId,
                    email=f"user{row.userId}@gmail.com",
                    password=f"password{row.userId}",
                )
                get_or_create(
                    session, models.Rating, user=user, movie=movie, rating=row.rating
                )

            session.commit()


if __name__ == "__main__":
    fill_db_with_movies()
    fill_db_with_ratings()
    print("Successfully filled database")
