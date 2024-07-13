import yfinance as yf
import pandas as pd
import pandas_ta as ta
import pytz

# Baixar dados históricos do ativo
ticker = "^SPX"
data = yf.download(ticker, start="2024-07-12", end="2024-07-13", interval="5m")
data.index = data.index.tz_convert('America/Sao_Paulo')

# Calcular o Parabolic SAR para identificar a direção da tendência
sar = ta.psar(data['High'], data['Low'], data['Close'])
# pd.DataFrame: long, short, af, and reversal columns.
# Configurar pandas para exibir todas as 100 linhas
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)
sar.rename(columns={sar.columns[0]: "SarLong", sar.columns[1]: "SarShort", sar.columns[2]: "Aceleration",
                    sar.columns[3]: "Reversion"}, inplace=True)

print(sar)
