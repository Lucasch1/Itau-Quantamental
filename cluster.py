import pandas as pd
from getData import *
import itertools
import statsmodels.api as sm
from sklearn.preprocessing import Normalizer
from sklearn.cluster import AgglomerativeClustering

tkrs = pd.read_csv('IBOV.csv')
tkrs = tkrs["Codigo"].tolist()
for i in range(len(tkrs)):
    tkrs[i] = tkrs[i] + ".SA"

start = '2021-01-01'
end = '2023-07-25'
df = getDataAdjClose(tkrs, start, end)

dfPct = df.pct_change()
dfPct = dfPct.dropna()
scaler = Normalizer().fit(dfPct)
pctNorm = scaler.transform(dfPct)
dfPctNorm = pd.DataFrame(pctNorm, columns=dfPct.columns, index=dfPct.index)
dfPctNormT = dfPctNorm.T

clustering = AgglomerativeClustering(n_clusters=17).fit(dfPctNormT)

dfCluster = pd.DataFrame(
    clustering.labels_, index=dfPctNorm.columns, columns=['Cluster'])

dfPivot = dfCluster.sort_values(by=['Cluster'])
print(dfPivot)

# Criar um dicionário para armazenar os ativos em cada cluster
cluster_dict = {}
for asset, cluster in zip(dfPivot.index, dfPivot['Cluster']):
    if cluster not in cluster_dict:
        cluster_dict[cluster] = []
    cluster_dict[cluster].append(asset)

# Criar o DataFrame final com os ativos por cluster
clusterDf = pd.DataFrame.from_dict(cluster_dict, orient='index').T
clusterDf.columns = [f'Cluster_{i}' for i in clusterDf.columns]
print(clusterDf)


pares_cointegrados = []

for col in clusterDf.columns:

    ativos = clusterDf[col].tolist()
    if len(ativos) >= 2:
        for ativo1, ativo2 in itertools.combinations(ativos, 2):
            if ativo1 != None and ativo2 != None:
                x = dfPct[ativo1]
                y = dfPct[ativo2]

                x = sm.add_constant(x)

                model = sm.OLS(y, x).fit()
                residuos = model.resid

                result = sm.tsa.adfuller(residuos)

                if result[1] < 0.05:
                    # print(
                    #     f'{ativo1} e {ativo2} são cointegrados com p-valor {result[1]}')
                    pares_cointegrados.append((ativo1, ativo2, result[1]))

pares_cointegrados.sort(key=lambda x: x[2])

with open('pares_cointegrados.csv', 'w') as arquivo:
    arquivo.write('Ativo 1;Ativo 2;Valor-p\n')
    for par in pares_cointegrados:
        arquivo.write(f'{par[0]};{par[1]};{par[2]}\n')

print("Pares cointegrados salvos em 'pares_cointegrados.csv'.")

cointegrados = pd.read_csv('pares_cointegrados.csv', sep=';')
print(cointegrados)
ratioPares = pd.DataFrame()
for i in range(len(cointegrados)):
    ratioPares[cointegrados['Ativo 1'][i] + '/' + cointegrados['Ativo 2']
               [i]] = df[cointegrados['Ativo 1'][i]] / df[cointegrados['Ativo 2'][i]]

print(ratioPares.head(50))
ratioPares.to_csv('ratioPares.csv', sep=';')
