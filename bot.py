from getData import *

tkr = input('Ativo desejado: ')
tkr = tkr.upper() + '.SA'

dat = getData(tkr, '2019-01-01', '2023-07-24')
dat = getSma(dat, 15)
print(dat.head(30))