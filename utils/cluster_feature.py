import numpy as np
import scipy.sparse as sp
import umap
import hdbscan
import pandas as pd


def cluster_feature(folder, feature='bert'):
    embedding = sp.load_npz(folder + f'new_{feature}_feature.npz').todense()
    embedding = np.asarray(embedding)

    feature_size = embedding[0].size
    # reducing the features before clustering them
    umap_embeddings = umap.UMAP(n_neighbors=15, n_components=5, metric='cosine').fit_transform(embedding)
    cluster = hdbscan.HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom').fit(
        umap_embeddings)

    # saving the cluster labels as a dataframe
    docs_df = pd.DataFrame()
    docs_df['Cluster'] = cluster.labels_
    docs_df['Doc_ID'] = range(len(embedding))

    # creating a mapping for each embedding to each cluster
    labels = np.unique(cluster.labels_)
    mapping_embedding2cluster = {}
    for index, row in docs_df.iterrows():
        if row.Cluster not in mapping_embedding2cluster:
            mapping_embedding2cluster[row.Cluster] = []
        mapping_embedding2cluster[row.Cluster].append(embedding[row.Doc_ID])

    for key in mapping_embedding2cluster.keys():
        mapping_embedding2cluster[key] = np.asarray(mapping_embedding2cluster[key])

    # make matrix for each cluster and then reduce it to a single vector containing the entire information
    for key in mapping_embedding2cluster.keys():
        mapping_t = mapping_embedding2cluster[key].T
        umap_embedding = umap.UMAP(n_neighbors=5, n_components=1, min_dist=0.0, metric='cosine').fit_transform(
            mapping_t)
        mapping_embedding2cluster[key] = umap_embedding.T
        mapping_embedding2cluster[key] = mapping_embedding2cluster[key].flatten()

    # create the concatenated matrix with the original matrix
    new_embedding = []
    for index, row in docs_df.iterrows():
        new_features = np.concatenate((embedding[row.Doc_ID], mapping_embedding2cluster[row.Cluster]), axis=0)
        assert (new_features.size == feature_size * 2)
        new_embedding.append(new_features)

    # saving the new embeddings are a sparse matrix format
    sparse_matrix = sp.csc_matrix(np.asarray(new_embedding))
    sp.save_npz(folder + f'new_{feature}_clustered_feature.npz', sparse_matrix)
