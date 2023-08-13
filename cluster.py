import pandas as pd
from getData import *
import itertools
import statsmodels.api as sm
from sklearn.preprocessing import Normalizer
from sklearn.cluster import AgglomerativeClustering

tkrs = pd.read_csv('IBOV.csv')
# print(tkrs["Codigo"].head())
tkrs = tkrs["Codigo"].tolist()
for i in range(len(tkrs)):
    tkrs[i] = tkrs[i] + ".SA"

start = '2021-01-01'
end = '2023-07-25'
df = getDataAdjClose(tkrs, start, end)
# print(df.head(50))

dfPct = df.pct_change()
dfPct = dfPct.dropna()
scaller = Normalizer().fit(dfPct)
pctNorm = scaller.transform(dfPct)
dfPctNorm = pd.DataFrame(pctNorm, columns=dfPct.columns, index=dfPct.index)

# print(dfPctNorm.head(50))

clustering = AgglomerativeClustering(n_clusters=5).fit(dfPctNorm)
# clustering.labels_
print(dfPctNorm.columns)
print(len(list(clustering.labels_)))
dfCluster = pd.DataFrame(
    clustering.labels_, index=dfPctNorm.columns, columns=['Cluster'])


# agrupamento - pd.DataFrame()
# for i, j in dfPctNorm.columns, clustering.labels_:
#    print(i, j)


print(dfCluster)
