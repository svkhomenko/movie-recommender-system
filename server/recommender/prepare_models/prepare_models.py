import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sqlmodel import Session
from database import engine
from .vectorization import (
    fetch_movies_data_for_vectorization,
    convert_to_proper_types,
    vectorization,
)
from .cluster_movies import cluster_movies
from .average_user_rating import (
    fetch_ratings_data,
    get_average_user_rating_for_movies_cluster,
)
from .fuzzy_cluster_users import fuzzy_cmeans_for_users

ARTIFACTS_DIR = Path(__file__).parent.parent.parent / "artifacts"


def prepare_models():
    if not ARTIFACTS_DIR.exists():
        ARTIFACTS_DIR.mkdir()

    with Session(engine) as session:
        movies_df = fetch_movies_data_for_vectorization(session)
        movies_df = convert_to_proper_types(movies_df)
        (
            movies_df,
            normalized_combined_features,
            doc2vec_model,
            count_vectorizer,
            optimal_svd_movie,
        ) = vectorization(movies_df)
        print("Successfully created vectorization models")
        doc2vec_model.save(str(ARTIFACTS_DIR / "doc2vec_model.model"))
        joblib.dump(count_vectorizer, ARTIFACTS_DIR / "cv_model.pkl")
        joblib.dump(optimal_svd_movie, ARTIFACTS_DIR / "svd_movie_model.pkl")

        movies_df, optimal_kmeans_combined = cluster_movies(
            movies_df, normalized_combined_features
        )
        print("Successfully cluster movies")
        joblib.dump(optimal_kmeans_combined, ARTIFACTS_DIR / "kmeans_movie_model.pkl")
        movies_df[["id", "cluster"]].to_csv(
            ARTIFACTS_DIR / "movie_clusters.csv", index=False
        )

        ratings_df = fetch_ratings_data(session)
        cluster_user_matrix = get_average_user_rating_for_movies_cluster(
            movies_df, ratings_df
        )
        membership_matrix, data_for_fcm_T, cntr, hard_labels, optimal_svd_user = (
            fuzzy_cmeans_for_users(cluster_user_matrix)
        )
        print("Successfully cluster users")
        membership_matrix_df = pd.DataFrame(
            membership_matrix,
            columns=[f"cluster_{i}" for i in range(membership_matrix.shape[1])],
        )
        membership_matrix_df.index = pd.Index(cluster_user_matrix.columns.values)
        membership_matrix_df.to_csv(ARTIFACTS_DIR / "user_membership_matrix.csv")

        np.save(ARTIFACTS_DIR / "user_feature_matrix.npy", data_for_fcm_T)
        np.save(ARTIFACTS_DIR / "user_cluster_centroids.npy", cntr)
        np.save(ARTIFACTS_DIR / "user_hard_labels.npy", hard_labels)

        user_ids = cluster_user_matrix.columns.values
        user_id_to_index = {user_id: idx for idx, user_id in enumerate(user_ids)}
        joblib.dump(user_id_to_index, ARTIFACTS_DIR / "user_id_to_index_map.pkl")
        joblib.dump(optimal_svd_user, ARTIFACTS_DIR / "svd_user_model.pkl")


if __name__ == "__main__":
    prepare_models()
