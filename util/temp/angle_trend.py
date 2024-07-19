import numpy as np
import pandas as pd
import yfinance as yf

# Baixar os dados
ticker = "^SPX"
data = yf.download(ticker, start="2024-07-01", end="2024-07-13", interval="5m")

# Converter o timezone de Datetime para o timezone de São Paulo
data.index = data.index.tz_convert("America/Sao_Paulo")


# Função para calcular o ângulo entre dois pontos
def calculate_angle(y1, y2, x_interval=1):
    slope = (y2 - y1) / x_interval
    angle_radians = np.arctan(slope)
    angle_degrees = np.degrees(angle_radians)
    return angle_degrees


# Adicionar nova coluna para os ângulos
angles = []
for i in range(len(data) - 1):
    y1 = data["Close"].iloc[i]
    y2 = data["Close"].iloc[i + 1]
    angle = calculate_angle(y1, y2)
    angles.append(angle)

# A última linha não terá um ângulo calculado
angles.append(np.nan)

data["Angle"] = angles

# Exibir os dados
pd.set_option("display.max_rows", 100)
data = data.round(2)
print(data.columns)

# Mostrar as últimas 100 linhas do DataFrame
print(data[["Close", "Angle"]].tail(78))
