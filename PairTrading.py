import pandas as pd
from getData import *
import itertools
import statsmodels.api as sm
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

pares_cointegrados = []

for ativo1, ativo2 in itertools.combinations(tkrs, 2):
    x = dfPct[ativo1]
    y = dfPct[ativo2]

    x = sm.add_constant(x)

    model = sm.OLS(y, x).fit()
    residuos = model.resid

    result = sm.tsa.adfuller(residuos)

    if result[1] < 0.05:
        pares_cointegrados.append((ativo1, ativo2, result[1]))

pares_cointegrados.sort(key=lambda x: x[2])


with open('pares_cointegrados.csv', 'w') as arquivo:
    arquivo.write('Ativo 1;Ativo 2;Valor-p\n')
    for par in pares_cointegrados:
        arquivo.write(f'{par[0]};{par[1]};{par[2]}\n')

print("Pares cointegrados salvos em 'pares_cointegrados.csv'.")

cointegrados = pd.read_csv('pares_cointegrados.csv', sep=';')
ratioPares = pd.DataFrame()
for i in range(len(cointegrados)):
    ratioPares[cointegrados['Ativo 1'][i] + '/' + cointegrados['Ativo 2']
               [i]] = df[cointegrados['Ativo 1'][i]] / df[cointegrados['Ativo 2'][i]]

print(ratioPares.head())
ratioPares.to_csv('ratioPares.csv', sep=';')
