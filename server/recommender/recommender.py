import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from gensim.models.doc2vec import Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from sqlmodel import Session, select, col, func
from database import engine
from .prepare_models.average_user_rating import fetch_ratings_data
from typing import Tuple, Sequence
from datetime import datetime, timedelta
import models
from models.movie import MoviePublic
import io
import sys
import re

ARTIFACTS_DIR = Path(__file__).parent.parent / "artifacts"
K_NEIGHBORS = 50
# TOP_N_FOR_FIS = 600
TOP_N_FOR_FIS = 200


class Recommender:
    _instance = None
    _is_initialized: bool = False

    def __new__(cls, artifacts_dir: Path = ARTIFACTS_DIR):
        if cls._instance is None:
            cls._instance = super(Recommender, cls).__new__(cls)
            cls._instance._load_artifacts(artifacts_dir)
            cls._instance._load_ratings()
            print("Ratings is loaded successfully")
            if cls._instance._is_initialized:
                cls._instance._setup_fuzzy_system()
                print("Fuzzy system setup completed successfully")
                cls._instance._create_movies_features_df()
            print("Recommender initialization completed successfully")
        return cls._instance

    def _load_ratings(self):
        with Session(engine) as session:
            self.ratings_df = fetch_ratings_data(session)

    def _load_artifacts(self, artifacts_dir: Path):
        if self._is_initialized:
            print("Recommender is already initialized. Skipping reinitializing")
            return

        print("Initializing and loading recommender system models")

        if not artifacts_dir.exists():
            raise FileNotFoundError(
                f"Artifacts folder not found: {artifacts_dir}. Please run prepare_models first: pipenv run python -m recommender.prepare_models.prepare_models"
            )

        try:
            self.normalized_movies_features = np.load(
                artifacts_dir / "normalized_features.npy"
            )
            # self.doc2vec_model = Doc2Vec.load(
            #     str(artifacts_dir / "doc2vec_model.model")
            # )
            # self.cv_model = joblib.load(artifacts_dir / "cv_model.pkl")
            # self.svd_movie_model = joblib.load(artifacts_dir / "svd_movie_model.pkl")

            # self.kmeans_movie_model = joblib.load(
            #     artifacts_dir / "kmeans_movie_model.pkl"
            # )
            self.movie_clusters_df = pd.read_csv(artifacts_dir / "movie_clusters.csv")

            # self.svd_user_model = joblib.load(artifacts_dir / "svd_user_model.pkl")
            self.user_membership_matrix_df = pd.read_csv(
                artifacts_dir / "user_membership_matrix.csv", index_col=0
            )
            self.user_id_to_index_map = joblib.load(
                artifacts_dir / "user_id_to_index_map.pkl"
            )

            self.user_feature_matrix = np.load(
                artifacts_dir / "user_feature_matrix.npy"
            )
            # self.user_cluster_centroids = np.load(
            #     artifacts_dir / "user_cluster_centroids.npy"
            # )
            self.user_hard_labels = np.load(artifacts_dir / "user_hard_labels.npy")

            self._is_initialized = True
            print("Artifacts loading completed successfully")

        except Exception as e:
            print(f"Failed to load artifacts: {e}")
            self._is_initialized = False

    def _setup_fuzzy_system(self):
        INP1_CosineSimilarity = ctrl.Antecedent(
            np.arange(0, 1.01, 0.01), "INP1_CosineSimilarity"
        )
        INP1_CosineSimilarity["low"] = fuzz.trapmf(
            INP1_CosineSimilarity.universe, [0, 0, 0.1, 0.3]
        )
        INP1_CosineSimilarity["medium"] = fuzz.trimf(
            INP1_CosineSimilarity.universe, [0.2, 0.3, 0.5]
        )
        INP1_CosineSimilarity["high"] = fuzz.trimf(
            INP1_CosineSimilarity.universe, [0.4, 0.55, 0.7]
        )
        INP1_CosineSimilarity["very_high"] = fuzz.trapmf(
            INP1_CosineSimilarity.universe, [0.6, 0.8, 1, 1]
        )

        INP2_ViewingHistory = ctrl.Antecedent(
            np.arange(0, 101, 1), "INP2_ViewingHistory"
        )
        INP2_ViewingHistory["very_recently"] = fuzz.trimf(
            INP2_ViewingHistory.universe, [0, 0, 20]
        )
        INP2_ViewingHistory["recently"] = fuzz.trimf(
            INP2_ViewingHistory.universe, [10, 25, 45]
        )
        INP2_ViewingHistory["long_ago"] = fuzz.trimf(
            INP2_ViewingHistory.universe, [35, 60, 95]
        )
        INP2_ViewingHistory["absent"] = fuzz.trimf(
            INP2_ViewingHistory.universe, [90, 100, 100]
        )

        INP3_Collection = ctrl.Antecedent(np.arange(0, 101, 1), "INP3_Collection")
        INP3_Collection["very_recently"] = fuzz.trimf(
            INP3_Collection.universe, [0, 0, 20]
        )
        INP3_Collection["recently"] = fuzz.trimf(INP3_Collection.universe, [10, 25, 45])
        INP3_Collection["long_ago"] = fuzz.trimf(INP3_Collection.universe, [35, 60, 95])
        INP3_Collection["absent"] = fuzz.trimf(INP3_Collection.universe, [90, 100, 100])

        INP4_WatchLater = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "INP4_WatchLater")
        INP4_WatchLater["no"] = fuzz.trapmf(INP4_WatchLater.universe, [0, 0, 0.1, 0.5])
        INP4_WatchLater["yes"] = fuzz.trapmf(
            INP4_WatchLater.universe, [0.5, 0.9, 1.0, 1.0]
        )

        INP5_AvgRating = ctrl.Antecedent(np.arange(0, 10.01, 0.01), "INP5_AvgRating")
        INP5_AvgRating["low"] = fuzz.trapmf(INP5_AvgRating.universe, [0, 0, 3, 4])
        INP5_AvgRating["medium"] = fuzz.trimf(INP5_AvgRating.universe, [3, 5, 7])
        INP5_AvgRating["high"] = fuzz.trapmf(INP5_AvgRating.universe, [6, 8, 10, 10])

        OUT1_Relevance = ctrl.Consequent(np.arange(0, 1.01, 0.01), "OUT1_Relevance")
        OUT1_Relevance["very_low"] = fuzz.trimf(OUT1_Relevance.universe, [0, 0, 0.3])
        OUT1_Relevance["low"] = fuzz.trimf(OUT1_Relevance.universe, [0.1, 0.3, 0.5])
        OUT1_Relevance["medium"] = fuzz.trimf(OUT1_Relevance.universe, [0.3, 0.5, 0.7])
        OUT1_Relevance["high"] = fuzz.trimf(OUT1_Relevance.universe, [0.5, 0.7, 0.9])
        OUT1_Relevance["very_high"] = fuzz.trimf(OUT1_Relevance.universe, [0.7, 1, 1])

        rules = []

        rules.append(
            ctrl.Rule(
                INP2_ViewingHistory["very_recently"] & INP3_Collection["very_recently"],
                OUT1_Relevance["very_high"],
            )
        )
        rules.append(
            ctrl.Rule(
                (INP1_CosineSimilarity["very_high"] | INP1_CosineSimilarity["high"])
                & INP5_AvgRating["high"],
                OUT1_Relevance["very_high"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["high"] & INP4_WatchLater["yes"],
                OUT1_Relevance["very_high"],
            )
        )
        rules.append(
            ctrl.Rule(
                (INP1_CosineSimilarity["very_high"] | INP1_CosineSimilarity["high"])
                & INP2_ViewingHistory["recently"],
                OUT1_Relevance["very_high"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP2_ViewingHistory["recently"] & INP5_AvgRating["high"],
                OUT1_Relevance["very_high"],
            )
        )

        rules.append(
            ctrl.Rule(
                (INP1_CosineSimilarity["medium"] | INP1_CosineSimilarity["high"])
                & INP3_Collection["recently"],
                OUT1_Relevance["high"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["medium"] & INP5_AvgRating["high"],
                OUT1_Relevance["high"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP4_WatchLater["yes"] & INP5_AvgRating["high"], OUT1_Relevance["high"]
            )
        )
        rules.append(
            ctrl.Rule(
                INP2_ViewingHistory["very_recently"] & INP5_AvgRating["medium"],
                OUT1_Relevance["high"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["medium"] & INP4_WatchLater["yes"],
                OUT1_Relevance["high"],
            )
        )

        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["medium"]
                & INP2_ViewingHistory["absent"]
                & INP4_WatchLater["no"]
                & INP5_AvgRating["medium"],
                OUT1_Relevance["medium"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["medium"] & INP3_Collection["long_ago"],
                OUT1_Relevance["medium"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["medium"] & INP5_AvgRating["medium"],
                OUT1_Relevance["medium"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP2_ViewingHistory["very_recently"] & INP5_AvgRating["low"],
                OUT1_Relevance["medium"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP2_ViewingHistory["recently"] & INP5_AvgRating["medium"],
                OUT1_Relevance["medium"],
            )
        )
        rules.append(
            ctrl.Rule(
                (INP2_ViewingHistory["very_recently"] | INP4_WatchLater["yes"])
                & (INP1_CosineSimilarity["low"] | INP5_AvgRating["low"]),
                OUT1_Relevance["medium"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["low"] & INP2_ViewingHistory["long_ago"],
                OUT1_Relevance["medium"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP3_Collection["absent"]
                & INP4_WatchLater["no"]
                & INP5_AvgRating["high"],
                OUT1_Relevance["medium"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["low"] & INP5_AvgRating["medium"],
                OUT1_Relevance["medium"],
            )
        )

        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["medium"] & INP5_AvgRating["low"],
                OUT1_Relevance["low"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["low"] & INP2_ViewingHistory["absent"],
                OUT1_Relevance["low"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["medium"] & INP5_AvgRating["low"],
                OUT1_Relevance["low"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["low"]
                & INP2_ViewingHistory["absent"]
                & INP3_Collection["long_ago"],
                OUT1_Relevance["low"],
            )
        )

        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["low"]
                & INP3_Collection["absent"]
                & INP5_AvgRating["low"],
                OUT1_Relevance["very_low"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["low"] & INP5_AvgRating["low"],
                OUT1_Relevance["very_low"],
            )
        )
        rules.append(
            ctrl.Rule(
                INP1_CosineSimilarity["low"]
                & INP2_ViewingHistory["absent"]
                & INP3_Collection["absent"],
                OUT1_Relevance["very_low"],
            )
        )

        self.relevance_system_ctrl = ctrl.ControlSystem(rules)
        self.relevance_simulation = ctrl.ControlSystemSimulation(
            self.relevance_system_ctrl
        )

    def _create_movies_features_df(self):
        features_df = (
            self.movie_clusters_df[["id"]].copy().rename(columns={"id": "movie_id"})
        )
        features_df["feature_vector"] = list(self.normalized_movies_features)
        features_df.set_index("movie_id", inplace=True)
        self.movies_features_df = features_df

    def is_ready(self) -> bool:
        return self._is_initialized

    def _get_user_cluster_index(self, user_id: int) -> int | None:
        if user_id not in self.user_id_to_index_map:
            return None

        matrix_index = self.user_id_to_index_map[user_id]
        cluster_index = self.user_hard_labels[matrix_index]
        return cluster_index

    def _find_weighted_neighbors(self, cur_user_id: int) -> list[Tuple[int, float]]:
        all_user_ids = np.array(list(self.user_id_to_index_map.keys()))

        try:
            u_idx = self.user_id_to_index_map[cur_user_id]
        except KeyError:
            return []

        user_feature_matrix = self.user_feature_matrix
        membership_matrix = self.user_membership_matrix_df.values
        hard_labels = self.user_hard_labels

        u_vector = user_feature_matrix[u_idx].reshape(1, -1)
        mu_u = membership_matrix[u_idx]

        Nc_quotas = np.round(K_NEIGHBORS * mu_u).astype(int)

        if Nc_quotas.sum() != K_NEIGHBORS:
            diff = K_NEIGHBORS - Nc_quotas.sum()
            Nc_quotas[np.argmax(Nc_quotas)] += diff

        all_neighbors = []

        for c_idx in range(membership_matrix.shape[1]):
            Nc = Nc_quotas[c_idx]
            cluster_indices = np.where(hard_labels == c_idx)[0]
            cluster_indices = cluster_indices[cluster_indices != u_idx]
            if Nc == 0 or len(cluster_indices) == 0:
                continue

            cluster_vectors = user_feature_matrix[cluster_indices]
            similarities = cosine_similarity(u_vector, cluster_vectors).flatten()

            if len(similarities) < Nc:
                top_indices = np.argsort(similarities)[::-1]
                Nc = len(similarities)
            else:
                top_indices = np.argsort(similarities)[-Nc:][::-1]

            top_neighbor_indices_in_matrix = cluster_indices[top_indices]
            top_neighbor_ids = all_user_ids[top_neighbor_indices_in_matrix]
            top_similarities = similarities[top_indices]

            for i in range(Nc):
                neighbor_id = top_neighbor_ids[i]
                sim = top_similarities[i]
                all_neighbors.append((neighbor_id, sim))

        return all_neighbors

    def _get_candidate_movies_ids(
        self, cur_user_id: int, neighbors: list[Tuple[int, float]]
    ) -> np.ndarray:
        user_ratings = self.ratings_df[self.ratings_df["user_id"] == cur_user_id]
        rated_movies_ids = user_ratings["movie_id"].unique()

        watched_ids: list[int] = []
        with Session(engine) as session:
            result_ids = session.exec(
                select(models.Watched.movie_id)
                .where(models.Watched.user_id == cur_user_id)
                .distinct()
            ).all()
            watched_ids = [id for id in result_ids if id is not None]

        neighbor_ids = [n[0] for n in neighbors]
        neighbor_ratings = self.ratings_df[
            self.ratings_df["user_id"].isin(neighbor_ids)
        ]
        all_neighbor_movies_ids = neighbor_ratings["movie_id"].unique()

        candidate_movies_ids = np.setdiff1d(
            all_neighbor_movies_ids, np.concatenate((rated_movies_ids, watched_ids))
        )
        return candidate_movies_ids

    def _predict_rating(
        self,
        movie_id: int,
        neighbors: list[Tuple[int, float]],
        neighbor_rating_lookup: dict[Tuple[int, int], float],
    ) -> float:
        numerator = 0.0
        denominator = 0.0

        for neighbor_id, sim_uv in neighbors:
            rating_vm = neighbor_rating_lookup.get((movie_id, neighbor_id))

            if rating_vm is not None:
                numerator += sim_uv * rating_vm
                denominator += sim_uv

        if denominator == 0:
            return 0.0

        predicted_rating = numerator / denominator
        return predicted_rating

    def _get_final_candidates_for_fis(
        self,
        cur_user_id: int,
        neighbors: list[Tuple[int, float]],
        candidate_movies_ids: np.ndarray,
    ) -> list[Tuple[int, float]]:
        neighbor_ids = [n[0] for n in neighbors]
        neighbor_rating_df = self.ratings_df[
            self.ratings_df["user_id"].isin(neighbor_ids)
        ][["user_id", "movie_id", "rating"]]

        neighbor_rating_lookup = neighbor_rating_df.set_index(["movie_id", "user_id"])[
            "rating"
        ].to_dict()

        predictions = {}

        for movie_id in candidate_movies_ids:
            predicted_rating = self._predict_rating(
                movie_id, neighbors, neighbor_rating_lookup
            )
            predictions[movie_id] = predicted_rating

        sorted_predicted_movies = sorted(
            predictions.items(), key=lambda item: item[1], reverse=True
        )

        positive_deviation_movies = [
            (movie_id, rating)
            for movie_id, rating in sorted_predicted_movies
            if rating >= 5.0
        ]

        negative_deviation_movies = [
            (movie_id, rating)
            for movie_id, rating in sorted_predicted_movies
            if rating < 5.0
        ]

        final_candidates_for_fis = []

        if len(positive_deviation_movies) <= TOP_N_FOR_FIS:
            final_candidates_for_fis.extend(positive_deviation_movies)
        else:
            final_candidates_for_fis.extend(positive_deviation_movies[:TOP_N_FOR_FIS])

        needed_count = TOP_N_FOR_FIS - len(final_candidates_for_fis)

        if needed_count > 0:
            candidates_to_add = negative_deviation_movies[:needed_count]
            final_candidates_for_fis.extend(candidates_to_add)

        return final_candidates_for_fis

    def _get_similarity_for_INP1(self, candidate_movie_id, ref_movie_ids):
        if not ref_movie_ids:
            return 0.0, 0.0

        try:
            candidate_vector = np.array(
                self.movies_features_df.loc[candidate_movie_id, "feature_vector"]
            ).reshape(1, -1)
        except KeyError:
            return 0.0, 0.0

        available_ids = [
            movie_id
            for movie_id in ref_movie_ids
            if movie_id in self.movies_features_df.index
        ]
        if not available_ids:
            return 0.0, 0.0

        ref_vectors_list = self.movies_features_df.loc[
            available_ids, "feature_vector"
        ].values
        ref_vectors_list = [np.array(vec) for vec in ref_vectors_list]
        ref_vectors_matrix = np.vstack(ref_vectors_list)

        cos_sim_vector = np.dot(ref_vectors_matrix, candidate_vector.T).flatten()

        return np.sum(cos_sim_vector), len(ref_vectors_list)

    def _get_vectorized_data_for_INP1_ratings(self, cur_user_id):
        user_ratings_df = self.ratings_df[
            self.ratings_df["user_id"] == cur_user_id
        ].copy()

        user_ratings_df.drop_duplicates(subset=["movie_id"], keep="last", inplace=True)
        user_ratings_df.reset_index(drop=True, inplace=True)

        rated_ids_with_features = user_ratings_df[
            user_ratings_df["movie_id"].isin(self.movies_features_df.index)
        ]["movie_id"]

        if rated_ids_with_features.empty:
            return np.array([]), np.array([])

        filtered_ratings = user_ratings_df[
            user_ratings_df["movie_id"].isin(rated_ids_with_features)
        ].set_index("movie_id")

        numpy_weights = filtered_ratings["rating"].values

        rated_vectors_list = self.movies_features_df.loc[
            filtered_ratings.index, "feature_vector"
        ].values  # type: ignore
        rated_vectors_matrix = np.vstack(rated_vectors_list)
        return rated_vectors_matrix, numpy_weights

    def _get_similarity_for_INP1_ratings(self, cur_user_id, candidate_movie_id):
        rated_vectors_matrix, numpy_weights = (
            self._get_vectorized_data_for_INP1_ratings(cur_user_id)
        )

        try:
            candidate_vector_2d = np.array(
                self.movies_features_df.loc[candidate_movie_id, "feature_vector"]
            ).reshape(1, -1)
        except KeyError:
            return 0.0, 0.0

        cos_sim_vector = np.dot(rated_vectors_matrix, candidate_vector_2d.T).flatten()
        numerator = np.sum(numpy_weights * cos_sim_vector)
        denominator = np.sum(np.abs(numpy_weights))
        return numerator, denominator

    def _calculate_INP1(
        self,
        cur_user_id,
        candidate_movie_id,
        viewing_history_movie_ids,
        watch_later_movie_ids,
    ):
        weightes = [0.5, 0.3, 0.2]

        ratings_numerator, ratings_denominator = self._get_similarity_for_INP1_ratings(
            cur_user_id, candidate_movie_id
        )
        viewing_history_numerator, viewing_history_denominator = (
            self._get_similarity_for_INP1(candidate_movie_id, viewing_history_movie_ids)
        )
        watch_later_numerator, watch_later_denominator = self._get_similarity_for_INP1(
            candidate_movie_id, watch_later_movie_ids
        )

        numerator = (
            ratings_numerator * weightes[0]
            + viewing_history_numerator * weightes[1]
            + watch_later_numerator * weightes[2]
        )
        denominator = (
            ratings_denominator * weightes[0]
            + viewing_history_denominator * weightes[1]
            + watch_later_denominator * weightes[2]
        )

        if denominator == 0:
            return 0.0

        INP1 = numerator / denominator
        return max(0, min(1, INP1))

    def _calculate_INP2(self, candidate_movie_id, viewing_history):
        created_at = viewing_history.get(candidate_movie_id)
        if not created_at:
            return 100

        time_difference = datetime.now() - created_at
        days_passed = time_difference.days
        return min(days_passed, 100)

    def _calculate_INP3(self, candidate_movie_id, viewing_history):
        days_passed = 100
        with Session(engine) as session:
            movie = session.get(models.Movie, candidate_movie_id)
            if not movie:
                return days_passed

            collection_ids = [collection.id for collection in movie.collections]
            if not collection_ids:
                return days_passed

            collection_movies_ids = session.exec(
                select(models.Movie.id)
                .join(models.MovieCollection)
                .where(col(models.MovieCollection.collection_id).in_(collection_ids))
                .distinct()
            ).all()

            for collection_movie_id in collection_movies_ids:
                created_at = viewing_history.get(collection_movie_id)
                if not created_at:
                    continue

                time_difference = datetime.now() - created_at
                days_passed = min(time_difference.days, days_passed)

            return days_passed

    def _calculate_INP4(self, candidate_movie_id, watch_later_movie_ids):
        if candidate_movie_id in watch_later_movie_ids:
            return 1.0
        return 0.0

    def _calculate_INP5(self, candidate_movie_id):
        with Session(engine) as session:
            movie = session.get(models.Movie, candidate_movie_id)
            if not movie:
                return 5.0

        return max(0.0, min(10.0, movie.vote_average))

    def _fis_input_preparation(self, cur_user_id, candidates_list):
        with Session(engine) as session:
            watch_later_ids = session.exec(
                select(models.Movie.id)
                .join(models.WatchLater)
                .where(models.WatchLater.user_id == cur_user_id)
                .distinct()
            ).all()

            time_cutoff = datetime.now() - timedelta(days=100)
            viewing_history_results = session.exec(
                select(
                    models.ViewingHistory.movie_id,
                    func.max(models.ViewingHistory.created_at).label("latest_view"),
                )
                .where(models.ViewingHistory.user_id == cur_user_id)
                .where(col(models.ViewingHistory.created_at) >= time_cutoff)
                .group_by(col(models.ViewingHistory.movie_id))
            ).all()

            viewing_history = {
                movie_id: latest_view
                for (movie_id, latest_view) in viewing_history_results
            }

        results = []
        viewing_history_ids = viewing_history.keys()

        for movie_id, _ in candidates_list:
            inp1 = self._calculate_INP1(
                cur_user_id=cur_user_id,
                candidate_movie_id=movie_id,
                viewing_history_movie_ids=viewing_history_ids,
                watch_later_movie_ids=watch_later_ids,
            )

            inp2 = self._calculate_INP2(movie_id, viewing_history)
            inp3 = self._calculate_INP3(movie_id, viewing_history)
            inp4 = self._calculate_INP4(movie_id, watch_later_ids)
            inp5 = self._calculate_INP5(movie_id)

            results.append(
                {
                    "movie_id": movie_id,
                    "INP1_CosineSimilarity": inp1,
                    "INP2_ViewingHistory": inp2,
                    "INP3_Collection": inp3,
                    "INP4_WatchLater": inp4,
                    "INP5_AvgRating": inp5,
                }
            )

        fis_input_df = pd.DataFrame(results)
        return fis_input_df

    def _get_final_candidates_after_fis(self, cur_user_id, final_candidates_for_fis):
        fis_data_for_ranking = self._fis_input_preparation(
            cur_user_id, final_candidates_for_fis
        )

        fis_data_for_ranking["OUT1_Relevance"] = 0.0
        recommendation_scores = []
        input_names = [
            "INP1_CosineSimilarity",
            "INP2_ViewingHistory",
            "INP3_Collection",
            "INP4_WatchLater",
            "INP5_AvgRating",
        ]

        for _, row in fis_data_for_ranking.iterrows():
            inputs = {name: row[name] for name in input_names}
            for name, value in inputs.items():
                self.relevance_simulation.input[name] = value

            try:
                self.relevance_simulation.compute()
                recommendation_scores.append(
                    self.relevance_simulation.output["OUT1_Relevance"]
                )
            except Exception as e:
                recommendation_scores.append(0.0)

        fis_data_for_ranking["OUT1_Relevance"] = recommendation_scores
        final_recommendations = fis_data_for_ranking.sort_values(
            by="OUT1_Relevance", ascending=False
        )
        return final_recommendations

    def _generate_fuzzy_result_explanation(self, rule_description):
        mapping = {
            "INP1_CosineSimilarity[very_high]": "similar to your taste",
            "INP1_CosineSimilarity[high]": "similar to your taste",
            "INP2_ViewingHistory[very_recently]": "viewed recently",
            "INP2_ViewingHistory[recently]": "viewed recently",
            "INP3_Collection[very_recently]": "in your series",
            "INP3_Collection[recently]": "in your series",
            "INP4_WatchLater[yes]": "Watch Later item",
            "INP5_AvgRating[high]": "high rating",
        }

        antecedent = rule_description.split(" THEN ")[0].replace("IF ", "")
        term_matches = re.findall(r"(\w+\[\w+\])", antecedent)
        explanations = []

        for term in term_matches:
            explanation = mapping.get(term)
            if explanation:
                explanations.append(explanation)

        if not explanations:
            return None

        if len(explanations) == 1:
            return explanations[0].capitalize()

        if len(explanations) > 1:
            unique_explanations = sorted(list(set(explanations)))

            result = ", ".join(unique_explanations[:-1])
            return result.capitalize()

        return None

    def _get_top_activated_rules_explanation(self, fis_data_row):
        input_names = [
            "INP1_CosineSimilarity",
            "INP2_ViewingHistory",
            "INP3_Collection",
            "INP4_WatchLater",
            "INP5_AvgRating",
        ]
        inputs = {name: fis_data_row[name] for name in input_names}

        try:
            for name, value in inputs.items():
                self.relevance_simulation.input[name] = value
            self.relevance_simulation.compute()
        except Exception:
            return None

        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        self.relevance_simulation.print_state()
        sys.stdout = old_stdout
        output_text = new_stdout.getvalue()

        activated_rules = []
        rules_list = self.relevance_system_ctrl.rules

        for rule_index, rule_object in enumerate(rules_list):
            rule_description = (
                f"IF {rule_object.antecedent} THEN {rule_object.consequent}"
            )

            rule_blocks = re.split(r"RULE #\d+:", output_text)[1:]

            if rule_index < len(rule_blocks):
                block = rule_blocks[rule_index]
                activation_match = re.search(
                    r"Activation \(THEN-clause\):.*?(\d+\.\d+)", block, re.DOTALL
                )

                strength = 0.0
                if activation_match:
                    try:
                        strength = float(activation_match.group(1))
                    except ValueError:
                        strength = 0.0

                is_high_relevance = (
                    "OUT1_Relevance[high]" in rule_description
                    or "OUT1_Relevance[very_high]" in rule_description
                )

                if strength > 0.5 and is_high_relevance:
                    activated_rules.append((strength, rule_description))

        if not activated_rules:
            return None

        activated_rules.sort(key=lambda x: x[0], reverse=True)
        top_rule_description = activated_rules[0][1]

        return self._generate_fuzzy_result_explanation(top_rule_description)

    def get_recommendations_explanation(
        self, movies: Sequence[models.Movie], recommendations_df: pd.DataFrame
    ):
        movies_public: list[MoviePublic] = []
        for movie in movies:
            try:
                fis_data_row = recommendations_df[
                    recommendations_df["movie_id"] == movie.id
                ].iloc[0]
                if fis_data_row["OUT1_Relevance"] > 0.5:
                    explanation = self._get_top_activated_rules_explanation(
                        fis_data_row
                    )
            except ValueError:
                explanation = None

            movie_data = movie.model_dump()
            movie_data["genres"] = movie.genres
            movie_data["explanation"] = explanation
            movie_data["collections"] = movie.collections
            movies_public.append(MoviePublic(**movie_data))

        return movies_public

    def get_recommendations(
        self, cur_user_id: int, num_recommendations: int = 50
    ) -> Tuple[list[int], pd.DataFrame]:
        if not self.is_ready():
            print(
                "The recommendation system is not ready. The artifacts are not loaded"
            )
            return [], pd.DataFrame()

        user_cluster_index = self._get_user_cluster_index(cur_user_id)

        if user_cluster_index is None:
            return [], pd.DataFrame()

        neighbors = self._find_weighted_neighbors(cur_user_id)
        if not neighbors:
            return [], pd.DataFrame()

        candidate_movies_ids = self._get_candidate_movies_ids(cur_user_id, neighbors)
        if len(candidate_movies_ids) == 0:
            return [], pd.DataFrame()

        final_candidates_for_fis = self._get_final_candidates_for_fis(
            cur_user_id, neighbors, candidate_movies_ids
        )

        final_candidates_df = self._get_final_candidates_after_fis(
            cur_user_id, final_candidates_for_fis
        )
        recommendation_list = final_candidates_df["movie_id"].tolist()
        return recommendation_list[:num_recommendations], final_candidates_df.head(
            num_recommendations
        )


RECOMMENDER_INSTANCE = Recommender()
