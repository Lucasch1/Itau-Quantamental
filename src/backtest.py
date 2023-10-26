import pandas as pd
import numpy as np


def pair_trading_strategy(data, pair_file, ratio_file):
    """
    Implements a pair trading strategy on historical data.

    Parameters:
    data (pd.DataFrame): Historical data to backtest on.
    pair_file (str): Path to CSV file containing pairs to trade.
    ratio_file (str): Path to CSV file containing ratios for each pair.
    max_exposition (float): Maximum exposition for each pair.

    Returns:
    pd.Series: Trading signals for the pair trading strategy.
    """
    # Load pairs from CSV file
    pairs = pd.read_csv(pair_file, sep=";")
    pairs = pd.DataFrame(pairs)

    # Load ratios from CSV file
    ratios = pd.read_csv(ratio_file, sep=";")

    # Initialize signals Series
    signals = pd.DataFrame(index=data["Date"])
    print(signals)

    # Loop over pairs
    for i, row in pairs.iterrows():
        # Extract pair data
        stock1, stock2 = row["Par"].split("/")
        ratio_mean = ratios[stock1 + "/" + stock2].mean()
        ratio_std = ratios[stock1 + "/" + stock2].std()

        # Calculate ratio
        ratio = data[stock1] / data[stock2]

        # Calculate z-score of ratio
        z_score = (ratio - ratio_mean) / ratio_std

        # Generate signals based on z-score and max exposition
        lis = []
        for z in z_score:
            if z > 0.05:
                lis.append(1)
            elif z == 0.00:
                lis.append(0)
            elif z < -0.05:
                lis.append(-1)
            else:
                lis.append("NaN")
        signals[f"{stock1}/{stock2}"] = lis

    return signals


def backtest(data, strategy, pair_file, ratio_file, max_exposition):
    """
    Backtests a trading strategy on historical data.

    Parameters:
    data (pd.DataFrame): Historical data to backtest on.
    strategy (function): Trading strategy to backtest.
    pair_file (str): Path to CSV file containing pairs to trade.
    ratio_file (str): Path to CSV file containing ratios for each pair.
    max_exposition (float): Maximum exposition for each pair.

    Returns:
    pd.DataFrame: Results of the backtest.
    """
    # Calculate signals using the strategy
    signals = strategy

    for i in pair_file["Par"]:
        stock1, stock2 = i.split("/")
        sig = signals[f"{stock1}/{stock2}"]
        status_LS = {
            "stock1": stock1,
            "stock2": stock2,
            "status": False,
            "status_1": False,
            "status_-1": False,
            "exposition": 0,
            "returns": 0,
            "stokc1_buy_price": [],
            "stock2_buy_price": [],
            "stock1_sell_price": [],
            "stock2_sell_price": [],
        }

        for i, j in sig.index, sig:
            if j == 1 and status_LS["status"] == False:
                status_LS.update({"status": True})
                status_LS["stock1_sell_price"].append(data[stock1][i])
                status_LS["stock2_buy_price"].append(data[stock2][i])
                status_LS["status_1"] = True
            elif j == 0 and status_LS["status"] == True:
                if status_LS["status_1"] == True:
                    status_LS.update({"status": False})
                    status_LS["stock1_buy_price"].append(data[stock1][i])
                    status_LS["stock2_sell_price"].append(data[stock2][i])
                    status_LS["status_1"] = False
                elif status_LS["status_-1"] == True:
                    status_LS.update({"status": False})
                    status_LS["stock1_sell_price"].append(data[stock1][i])
                    status_LS["stock2_buy_price"].append(data[stock2][i])
                    status_LS["status_-1"] = False
            elif j == -1 and status_LS["status"] == False:
                status_LS.update({"status": True})
                status_LS["stock1_buy_price"].append(data[stock1][i])
                status_LS["stock2_sell_price"].append(data[stock2][i])
                status_LS["status_-1"] = True

    # Calculate returns based on the signals
    returns = signals.shift(1) * data["returns"]

    # Calculate cumulative returns
    cumulative_returns = (1 + returns).cumprod()

    # Calculate drawdowns
    max_returns = cumulative_returns.cummax()
    drawdowns = (cumulative_returns - max_returns) / max_returns

    # Combine results into a DataFrame
    results = pd.DataFrame(
        {
            "signals": signals,
            "returns": returns,
            "cumulative_returns": cumulative_returns,
            "drawdowns": drawdowns,
        }
    )

    return results


def main():
    data = pd.read_csv("src/database/mkt_data.csv")
    pair_file_path = "src/output/MeanReverting.csv"
    pair_file = pd.read_csv(pair_file_path, sep=";")
    ratio_file_path = "src/output/ratioPares.csv"
    ratio_file = pd.read_csv(ratio_file_path, sep=";")
    exposition = 1000000.00

    signals = pair_trading_strategy(data, pair_file_path, ratio_file_path)
    print(signals)

    test = backtest(data, signals, pair_file, ratio_file, exposition)

    print(test)


if __name__ == "__main__":
    main()
