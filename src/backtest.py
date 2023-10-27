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
    # print(signals)

    # Loop over pairs
    for i, row in pairs.iterrows():
        # Extract pair data
        stock1, stock2 = row["Par"].split("/")
        ratio_mean = ratios[stock1 + "/" + stock2].mean()
        # ratio_std = ratios[stock1 + "/" + stock2].std()

        # Calculate ratio
        # ratio = data[stock1] / data[stock2]
        # print("ratio:", ratio)

        # Calculate z-score of ratio
        # z_score = (ratio - ratio_mean) / ratio_std

        # Generate signals based on z-score and max exposition
        lis = []
        for z in ratios[stock1 + "/" + stock2]:
            if z > (1.05 * ratio_mean):
                lis.append(1)
            elif (ratio_mean * 1.01) > z > (0.99 * ratio_mean):
                lis.append(0)
            elif z < (0.95 * ratio_mean):
                lis.append(-1)
            else:
                # print(z)
                lis.append(2)
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
    print(signals.head(100))
    resultados = []

    for i in pair_file["Par"]:
        stock1, stock2 = i.split("/")
        sig = signals[f"{stock1}/{stock2}"]
        status_LS = {
            "Name": f"{stock1}/{stock2}",
            "stock1": stock1,
            "stock2": stock2,
            "status": False,
            "status_1": False,
            "status_-1": False,
            "exposition_stock1": 0,
            "exposition_stock2": 0,
            "returns_total": 0,
            "stock1_buy_price": [],
            "stock2_buy_price": [],
            "stock1_sell_price": [],
            "stock2_sell_price": [],
            "returns": [],
            "returns_Dates": [],
            "ls_counter": 0,
        }
        
        for i, j in signals.iterrows():
            if j[f"{stock1}/{stock2}"] == 1 and status_LS["status"] == False:
                # print(data.loc[data["Date"] == i, stock1])
                if float(data.loc[data["Date"] == i, stock1]) == 0.00 or float(data.loc[data["Date"] == i, stock2]) == 0.00:
                    print("zerou")
                else:
                    status_LS["status"] = True
                    status_LS["status_1"] = True
                    status_LS["stock1_sell_price"].append(float(data.loc[data["Date"] == i, stock1]))
                    status_LS["stock2_buy_price"].append(float(data.loc[data["Date"] == i, stock2]))

                    # LOGICA DE EXPOSICAO E LOGICA DE RETURNS
                    status_LS["exposition_stock1"] = -100.00 * float(data.loc[data["Date"] == i, stock1])
                    status_LS["exposition_stock2"] = 100.00 * float(data.loc[data["Date"] == i, stock2])
                    status_LS["returns_Dates"].append([str(i)])


            elif j[f"{stock1}/{stock2}"] == 0 and status_LS["status"] == True:
                if status_LS["status_1"] == True:
                    #Precos de compra e venda das acoes
                    status_LS["stock1_buy_price"].append(float(data.loc[data["Date"] == i, stock1]))                 
                    status_LS["stock2_sell_price"].append(float(data.loc[data["Date"] == i, stock2]))

                    # LOGICA DE EXPOSICAO E LOGICA DE RETURNS
                    profit_stock1 = status_LS["exposition_stock1"] + 100 * float(data.loc[data["Date"] == i, stock1])
                    profit_stock2 = status_LS["exposition_stock2"] - 100 * float(data.loc[data["Date"] == i, stock1])
                    profit = profit_stock1 + profit_stock2
                    status_LS["returns_total"] = status_LS["returns_total"] + profit
                    status_LS["returns"].append(profit)
                    status_LS["exposition_stock1"] = 0
                    status_LS["exposition_stock2"] = 0
                    
                    #Conclusao
                    status_LS["status_1"] = False
                    status_LS["status"] = False
                    status_LS["returns_Dates"][int(status_LS["ls_counter"])].append(str(i))
                    status_LS["ls_counter"] = status_LS["ls_counter"] + 1
                    


                elif status_LS["status_-1"] == True:
                    #Precos de compra e venda das acoes
                    status_LS["stock1_sell_price"].append(float(data.loc[data["Date"] == i, stock1]))
                    status_LS["stock2_buy_price"].append(float(data.loc[data["Date"] == i, stock2]))
                    
                    # LOGICA DE EXPOSICAO E LOGICA DE RETURNS
                    profit_stock1 = status_LS["exposition_stock1"] - 100 * float(data.loc[data["Date"] == i, stock1])
                    profit_stock2 = status_LS["exposition_stock2"] + 100 * float(data.loc[data["Date"] == i, stock1])
                    profit = profit_stock1 + profit_stock2
                    status_LS["returns_total"] = status_LS["returns_total"] + profit
                    status_LS["returns"].append(profit)
                    status_LS["exposition_stock1"] = 0
                    status_LS["exposition_stock2"] = 0

                    #Conclusao
                    status_LS["status_-1"] = False
                    status_LS["status"] = False
                    status_LS["returns_Dates"][status_LS["ls_counter"]].append(str(i))
                    status_LS["ls_counter"] = status_LS["ls_counter"] + 1

                    # LOGICA DE EXPOSICAO E LOGICA DE RETURNS

            elif j[f"{stock1}/{stock2}"] == -1 and status_LS["status"] == False:
                if int(data.loc[data["Date"] == i, stock1]) == 0 or int(data.loc[data["Date"] == i, stock2]) == 0:
                    print("zerou")
                else:
                    status_LS["status"] = True
                    status_LS["stock1_buy_price"].append(float(data.loc[data["Date"] == i, stock1]))
                    status_LS["stock2_sell_price"].append(float(data.loc[data["Date"] == i, stock2]))
                    status_LS["status_-1"] = True

                    status_LS["status"] = True
                    status_LS["status_-1"] = True
                    status_LS["stock1_buy_price"].append(float(data.loc[data["Date"] == i, stock1]))
                    status_LS["stock2_sell_price"].append(float(data.loc[data["Date"] == i, stock2]))

                    # LOGICA DE EXPOSICAO E LOGICA DE RETURNS
                    status_LS["exposition_stock1"] = 100.00 * float(data.loc[data["Date"] == i, stock1])
                    status_LS["exposition_stock2"] = -100.00 * float(data.loc[data["Date"] == i, stock2])
                    status_LS["returns_Dates"].append([str(i)])



        resultados.append(status_LS)
    print(resultados[0])


    return resultados


def main():
    data = pd.read_csv("src/database/mkt_data.csv", sep=",")
    pair_file_path = "src/output/MeanReverting.csv"
    pair_file = pd.read_csv(pair_file_path, sep=";")
    ratio_file_path = "src/output/ratioPares.csv"
    ratio_file = pd.read_csv(ratio_file_path, sep=";")
    exposition = 1000000.00

    signals = pair_trading_strategy(data, pair_file_path, ratio_file_path)
    # print(signals)

    test = backtest(data, signals, pair_file, ratio_file, exposition)

    # print(test)


if __name__ == "__main__":
    main()
