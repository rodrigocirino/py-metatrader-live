import yfinance as yf
import pandas as pd
import pandas_ta as ta
import pytz
import os

# Baixar dados históricos do ativo
ticker = "^SPX"
data = yf.download(ticker, start="2024-07-01", end="2024-07-13", interval="5m")

# Converter o timezone de Datetime para o timezone de São Paulo
data.index = data.index.tz_convert('America/Sao_Paulo')

# Calcular o Aroon (Aroon Up e Aroon Down) para medir a força da tendência
aroon = ta.aroon(data['High'], data['Low'], length=14)
data['Aroon_Up'] = aroon['AROONU_14']
data['Aroon_Down'] = aroon['AROOND_14']


# Definir a força da tendência com base nos valores do Aroon
def define_trend_strength(aroon_up, aroon_down):
    if aroon_up > 80 and aroon_down < 20:
        return "Forte Alta"
    elif aroon_down > 80 and aroon_up < 20:
        return "Forte Baixa"
    elif (50 <= aroon_up <= 80 and aroon_down < 50) or (50 <= aroon_down <= 80 and aroon_up < 50):
        return "Médio"
    else:
        return "Neutro"


# Aplicar a função define_trend_strength para cada par de valores Aroon Up e Aroon Down e criar uma nova coluna
data['Trend_Strength'] = data.apply(lambda row: define_trend_strength(row['Aroon_Up'], row['Aroon_Down']), axis=1)

# Arredondar todas as colunas numéricas para 2 dígitos
data = data.round(2)

# Configurar pandas para exibir todas as 100 linhas
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 20)

# Mostrar as últimas 100 linhas do DataFrame
print(data[['Close', 'Aroon_Up', 'Aroon_Down', 'Trend_Strength']].tail(78))

# record a file
os.makedirs("export", exist_ok=True)
data.to_csv(f"export/aroon.csv")
