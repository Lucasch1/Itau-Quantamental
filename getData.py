import yfinance as yf
import pandas as pd

def getData(tiker, start, end):
    data = yf.download(tiker, start=start, end=end)
    data = pd.DataFrame(data)
    return data

def getClose(data):
    return data['Close']