import pandas as pd
import yfinance as yf


def get_market_data(
    start: str, end: str, tickers: str | list[str] = None
) -> pd.DataFrame:
    print("Gostaria de baixar novos dados?")
    print("1 - Sim")
    print("2 - Não")
    i = int(input())
    if i == 1:
        if isinstance(tickers, str):
            tickers = [tickers]
        if tickers is None:
            tickers = pd.read_csv("src/database/IBOV.csv")
            tickers = tickers["Codigo"].tolist()
        tickers = [ticker + ".SA" for ticker in tickers]
        df = yf.download(tickers, start, end)["Adj Close"]
        df.to_csv("src/database/mkt_data.csv")
    else:
        df = pd.read_csv("src/database/mkt_data.csv")
        df.set_index("Date", inplace=True)
    # try:
    #     df = pd.read_csv("src/database/mkt_data.csv")
    #     df.set_index("Date", inplace=True)
    # except:
    #     if isinstance(tickers, str):
    #         tickers = [tickers]
    #     if tickers is None:
    #         tickers = pd.read_csv("src/database/IBOV.csv")
    #         tickers = tickers["Codigo"].tolist()
    #     tickers = [ticker + ".SA" for ticker in tickers]
    #     df = yf.download(tickers, start, end)["Adj Close"]
    #     df.to_csv("src/database/mkt_data.csv")
    return df
