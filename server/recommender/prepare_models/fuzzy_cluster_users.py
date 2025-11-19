import numpy as np
from sklearn.decomposition import TruncatedSVD
import skfuzzy as fuzz


def fuzzy_cmeans_for_users(cluster_user_matrix):
    n_components_optimal = 22
    optimal_svd = TruncatedSVD(n_components=n_components_optimal, random_state=42)
    data_for_svd = cluster_user_matrix.values.T
    svd_result = optimal_svd.fit_transform(data_for_svd)
    data_for_fcm = svd_result.T

    n_clusters = 4
    m_fuzzifier = 2
    max_iter = 100
    error = 0.0001

    cntr, u, u0, d, jm, p, fpc = fuzz.cmeans(
        data_for_fcm, n_clusters, m_fuzzifier, error=error, maxiter=max_iter, init=None
    )

    membership_matrix = u.T
    hard_labels = np.argmax(membership_matrix, axis=1)
    data_for_fcm_T = svd_result
    return membership_matrix, data_for_fcm_T, cntr, hard_labels, optimal_svd
