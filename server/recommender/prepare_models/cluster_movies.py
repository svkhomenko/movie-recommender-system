from sklearn.cluster import KMeans


def cluster_movies(movies_df, normalized_combined_features):
    optimal_n_clusters = 35
    optimal_kmeans_combined = KMeans(
        n_clusters=optimal_n_clusters, n_init=10, random_state=42
    )
    final_cluster_labels_combined = optimal_kmeans_combined.fit_predict(
        normalized_combined_features
    )

    movies_df["cluster"] = final_cluster_labels_combined
    return movies_df, optimal_kmeans_combined
