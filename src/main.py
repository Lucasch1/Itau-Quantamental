import os
import sys
from domain import calcs

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
    normal = calcs.check_normality(ratios)
    pass

if __name__ == "__main__":
    main()
