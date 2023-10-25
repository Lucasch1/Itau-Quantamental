import os
import sys
from domain import calcs
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import mkt_data
from src.domain import clustering, pre_processing


def main():
    start = "2021-01-01"
    end = "2023-07-25"

    df = mkt_data.get_market_data(start, end)
    df_pct = df.pct_change()
    df_pct = df_pct.dropna()

    train, test = pre_processing.split_train_test_data(df_pct)
    
    cluster = clustering.cluster_data(df_pct)
    pares_cointegrados = calcs.cointegrate_data(cluster, df_pct)

    calcs.save_coint_pairs(pares_cointegrados)
    ratios = calcs.calc_and_save_ratios(df)
    normal, normalDf = calcs.check_normality(ratios)

    listaTempoMedioReversao = []
    listaNomePar = []
    for i in range(0, 15):
        tempo_medio_reversao = calcs.checkMeanReverting(ratios[normalDf.index[i]])
        listaTempoMedioReversao.append(tempo_medio_reversao)
        listaNomePar.append(normalDf.index[i])

    resultado_df = pd.DataFrame(
        {"Par": listaNomePar, "Tempo Medio de Reversao": listaTempoMedioReversao}
    )
    resultado_df = resultado_df[resultado_df["Tempo Medio de Reversao"] > 0]
    resultado_df = resultado_df.sort_values(by="Tempo Medio de Reversao")
    resultado_df.to_csv("src/output/MeanReverting.csv", sep=";")
    print(train, test)


if __name__ == "__main__":
    main()
