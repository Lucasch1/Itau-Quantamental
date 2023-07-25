import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np


def getData(tiker, start, end):
    data = yf.download(tiker, start=start, end=end)
    data = pd.DataFrame(data)
    return data

def getSma(data, period):
    data[f'SMA-{period}'] = ta.sma(data['Close'], length=period)
    return data
