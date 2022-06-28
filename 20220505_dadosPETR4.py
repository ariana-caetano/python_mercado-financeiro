#importando as bibliotecas
import yfinance as yf
import matplotlib.pyplot as plt
import pandas_datareader.data as web


#este código vai consultar os dados de PETR4 no ano de 2021
#e exibirá um gráfico de linhas com os preços de fechamento do ativo
# e médias móveis de 9 exponencial e 21 aritmética


#sobrescrevendo os métodos do panda_datareader 
yf.pdr_override()

#baixando dados PETR4
#consultar os ticker no site https://finance.yahoo.com/

codigoAcao = 'PETR4.SA'
dataInicial = "2021-01-01"
dataFinal = "2021-12-31"
ativo = web.get_data_yahoo(codigoAcao, start = dataInicial, end = dataFinal)

#print(ativo.dtypes)

#tratando os dados de forma bem simples
#removendo espaços
#tudo em minúsculas
#sem acento
#regra de normalização
#existem vários outros tratamentos a serem feitos tbm nos dados e é importante sempre fazer o tratamento
ativo.columns = ativo.columns.str.replace('\s+', '_', regex=True)
ativo.columns = ativo.columns.str.lower()
ativo.columns = ativo.columns.str.replace(r'[^\w\s]+', '_', regex=True)
ativo.columns = ativo.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

#calculando a média móvel de 21 períodos (fechamento)

df = ativo[["close"]]
#método rolling retorna uma janela de período n (21) e o método mean() calcula a média
df["mma21"] = df["close"].rolling(window=21).mean()

#calculando média de 9 exponencial
df["mme9"] = df["close"].ewm(span=9, min_periods=9).mean()


# Preço de fechamento
df["close"].plot(figsize=(20, 5), label="PETR4")
# Média móvel 21 dias
df["mma21"].plot(label="mma-21")
# Média móvel 9 dias
df["mme9"].plot(label="mme-9")
# Legendas
plt.legend()
plt.show()
