import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np


def getData(tiker, start, end):
    data = yf.download(tiker, start=start, end=end)
    data = pd.DataFrame(data)
    return data


def getDataAdjClose(tiker, start, end):
    data = yf.download(tiker, start=start, end=end)['Adj Close']
    return data


def getSma(data, period):
    data[f'SMA-{period}'] = ta.sma(data['Close'], length=period)
    return data


def getCorrel(df1, df2):
    df1 = df1['Close']
    df2 = df2['Close']
    corr = df1.corr(df2)
    return corr
