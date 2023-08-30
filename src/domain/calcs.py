import pandas as pd
import itertools
import statsmodels.api as sm
from scipy.stats import shapiro

def cointegrate_data(
    cluster_df: pd.DataFrame, df_pct: pd.DataFrame
) -> list[tuple[str, str, float]]:
    pares_cointegrados = []

    for col in cluster_df.columns:
        ativos = cluster_df[col].tolist()
        if len(ativos) >= 2:
            for ativo1, ativo2 in itertools.combinations(ativos, 2):
                if ativo1 != None and ativo2 != None:
                    x = df_pct[ativo1]
                    y = df_pct[ativo2]

                    x = sm.add_constant(x)

                    model = sm.OLS(y, x).fit()
                    residuos = model.resid

                    result = sm.tsa.adfuller(residuos)

                    if result[1] < 0.05:
                        pares_cointegrados.append((ativo1, ativo2, result[1]))

    pares_cointegrados.sort(key=lambda x: x[2])

    return pares_cointegrados


def save_coint_pairs(pares_cointegrados: list[tuple[str, str, float]]) -> None:
    with open("src/output/pares_cointegrados.csv", "w") as arquivo:
        arquivo.write("Ativo 1;Ativo 2;Valor-p\n")
        for par in pares_cointegrados:
            arquivo.write(f"{par[0]};{par[1]};{par[2]}\n")


def calc_and_save_ratios(df: pd.DataFrame) -> pd.DataFrame:
    cointegrados = pd.read_csv("src/output/pares_cointegrados.csv", sep=";")
    ratio_pares = pd.DataFrame()
    for i in range(len(cointegrados)):
        ratio_pares[cointegrados["Ativo 1"][i] + "/" + cointegrados["Ativo 2"][i]] = (
            df[cointegrados["Ativo 1"][i]] / df[cointegrados["Ativo 2"][i]]
        )

    print(ratio_pares.head(50))
    ratio_pares.to_csv("src/output/ratioPares.csv", sep=";")
    return ratio_pares

def check_normality(ratios: pd.DataFrame) -> dict[str, float]:
    check = ratios.copy()
    normal = {}
    for col in check.columns:
        test = shapiro(check[col].values)
        if test.pvalue > 0.05:
            normal[col] = test.pvalue

    return normal
    
