import yfinance as yf
import pandas as pd
import pandas_ta as ta

tkr = input('Ativo desejado: ')
tkr = tkr.upper() + '.SA'

def getData(tiker, start, end):
    data = yf.download(tiker, start=start, end=end)
    data = pd.DataFrame(data)
    return data

def getSma(data, period):
    data[f'SMA-{period}'] = ta.sma(data['Close'], length=period)
    return data

dat = getData(tkr, '2019-01-01', '2023-07-24')
dat = getSma(dat, 15)
print(dat)