from getData import *

print('Bem vindo ao bot de análise de ativos!')
print('Para comecar escolha o que deseja fazer:')
print('1 - Verificar correlação entre ativos')
print('2 - Verificar SMA de um ativo')

op = input('Opção: ')

if op == '1':
    tkr1 = input('Ativo 1: ')
    tkr2 = input('Ativo 2: ')
    tkr1 = tkr1.upper() + '.SA'
    tkr2 = tkr2.upper() + '.SA'
    dat1 = getData(tkr1, '2019-01-01', '2023-07-24')
    dat2 = getData(tkr2, '2019-01-01', '2023-07-24')
    corr = getCorrel(dat1, dat2)
    print(f'A correlação entre {tkr1} e {tkr2} é de {corr}')

elif op == '2':
    tkr = input('Ativo desejado: ')
    tkr = tkr.upper() + '.SA'
    dat = getData(tkr, '2019-01-01', '2023-07-24')
    dat = getSma(dat, 15)
    print(dat.head(30))

