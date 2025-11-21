import pandas as pd
from sqlmodel import Session, select
import models


def fetch_ratings_data(session: Session) -> pd.DataFrame:
    result = session.exec(
        select(models.Rating.user_id, models.Rating.movie_id, models.Rating.rating)
    )

    ratings_tuples = result.all()
    ratings_df = pd.DataFrame(ratings_tuples, columns=["user_id", "movie_id", "rating"])
    return ratings_df


def get_average_user_rating_for_movies_cluster(movies_df, ratings_df):
    movie_cluster_map = movies_df[["id", "cluster"]].rename(columns={"id": "movie_id"})
    ratings_with_cluster = pd.merge(
        ratings_df, movie_cluster_map, on="movie_id", how="inner"
    )

    user_avg_rating = (
        ratings_with_cluster.groupby("user_id")["rating"].mean().rename("r_avg")
    )
    ratings_with_cluster = pd.merge(ratings_with_cluster, user_avg_rating, on="user_id")
    ratings_with_cluster["r_d"] = (
        ratings_with_cluster["rating"] - ratings_with_cluster["r_avg"]
    )

    cluster_agg = ratings_with_cluster.groupby("cluster").agg(
        sum_r_d=("r_d", "sum"), count_ratings=("r_d", "count")
    )
    cluster_agg["Cc"] = cluster_agg["sum_r_d"] / cluster_agg["count_ratings"]
    Cc_map = cluster_agg["Cc"]

    user_cluster_agg = (
        ratings_with_cluster.groupby(["user_id", "cluster"])
        .agg(sum_r_d_user=("r_d", "sum"), count_ratings_user=("r_d", "count"))
        .reset_index()
    )
    user_cluster_agg["Cc"] = user_cluster_agg["cluster"].map(Cc_map)

    a = 20
    user_cluster_agg["r_c"] = (
        user_cluster_agg["sum_r_d_user"] + a * user_cluster_agg["Cc"]
    ) / (user_cluster_agg["count_ratings_user"] + a)
    cluster_user_matrix = user_cluster_agg.pivot(
        index="cluster", columns="user_id", values="r_c"
    ).fillna(0)

    all_user_ids_array = cluster_user_matrix.columns.values
    user_id_to_index = {
        user_id: index for index, user_id in enumerate(all_user_ids_array)
    }

    return cluster_user_matrix
