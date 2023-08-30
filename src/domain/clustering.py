import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import Normalizer


def cluster_data(df: pd.DataFrame, n_clusters: int = 17) -> pd.DataFrame:
    scaler = Normalizer().fit(df)
    pct_norm = scaler.transform(df)
    df_pct_norm = pd.DataFrame(pct_norm, columns=df.columns, index=df.index)
    df_pct_norm_t = df_pct_norm.T

    clustering = AgglomerativeClustering(n_clusters).fit(df_pct_norm_t)

    df_cluster = pd.DataFrame(
        clustering.labels_, index=df_pct_norm.columns, columns=['Cluster'])
    
    df_pivot = df_cluster.sort_values(by=['Cluster'])

    cluster_dict = {}
    for asset, cluster in zip(df_pivot.index, df_pivot['Cluster']):
        if cluster not in cluster_dict:
            cluster_dict[cluster] = []
        cluster_dict[cluster].append(asset)

    cluster_df = pd.DataFrame.from_dict(cluster_dict, orient='index').T
    cluster_df.columns = [f'Cluster_{i}' for i in cluster_df.columns]

    return cluster_df
