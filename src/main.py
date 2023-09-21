import os
import sys
from domain import calcs
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import mkt_data
from src.domain import clustering


def main():
    start = "2021-01-01"
    end = "2023-07-25"

    df = mkt_data.get_market_data(start, end)
    df_pct = df.pct_change()
    df_pct = df_pct.dropna()

    cluster = clustering.cluster_data(df_pct)
    pares_cointegrados = calcs.cointegrate_data(cluster, df_pct)

    calcs.save_coint_pairs(pares_cointegrados)
    ratios = calcs.calc_and_save_ratios(df)
    normal, normalDf = calcs.check_normality(ratios)
    # print(normalDf)
    listaTaxaReversao = []
    listaTempoMedioReversao = []
    listaNomePar = []
    for i in range(0, 15):
        taxa_reversao, tempo_medio_reversao = calcs.checkMeanReverting(ratios[normalDf.index[i]]) 
        # print(normalDf.index[i], taxa_reversao, tempo_medio_reversao)
        listaTaxaReversao.append(taxa_reversao)
        listaTempoMedioReversao.append(tempo_medio_reversao)
        listaNomePar.append(normalDf.index[i])

    resultado_df = pd.DataFrame({
        'Par': listaNomePar,
        'Taxa de Reversao': listaTaxaReversao,
        'Tempo Medio de Reversao': listaTempoMedioReversao
    })
    resultado_df = resultado_df.sort_values(by='Taxa de Reversao', ascending=False)
    resultado_df.to_csv("src/output/MeanReverting.csv", sep=";")
    pass

if __name__ == "__main__":
    main()
