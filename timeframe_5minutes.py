import MetaTrader5 as mt5
import pandas as pd

# Inicializar o MetaTrader 5
if not mt5.initialize():
    print("Failed to initialize MetaTrader 5")
    mt5.shutdown()
    exit()

# Definir o símbolo e o timeframe
symbol = "WIN$D"
timeframe = mt5.TIMEFRAME_M5
num_bars = 10000  # número de barras de dados para recuperar

# Obter os dados OHLC
bars = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)

# Desconectar do MetaTrader 5
mt5.shutdown()

# Verificar se os dados foram obtidos
if bars is None:
    print("Failed to get OHLC data")
    exit()

# Converter para DataFrame do pandas
df = pd.DataFrame(bars)

# Converter o timestamp para datetime
df['time'] = pd.to_datetime(df['time'], unit='s')

# Definir a coluna 'time' como índice
df.set_index('time', inplace=True)

# Exibir o DataFrame
print(df)
