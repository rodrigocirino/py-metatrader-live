import time

import MetaTrader5 as mt5

# Inicializa a conexão com o terminal MetaTrader 5
if not mt5.initialize():
    print("initialize() falhou")
    mt5.shutdown()
    exit()

# Defina o símbolo
TICKER = "VALE3"
# print(f"{'Ticker'.ljust(8)} {'Last'.ljust(10)} {'Volume'.ljust(12)} {'Bid'.ljust(10)} {'Ask'.ljust(10)}".upper())
print(f"{'Ticker'.ljust(8)} {'Last'.ljust(10)} {'Volume'.ljust(12)}".upper())

while True:
    # Obtenha informações sobre o símbolo
    symbol_data = mt5.symbol_info(TICKER)
    if symbol_data is None:
        print(f"Não foi possível obter informações sobre o símbolo {TICKER}")
    else:
        # print(f"{symbol_data.name.ljust(8)} {str(symbol_data.last).ljust(10)} {str(symbol_data.session_volume).ljust(12)} {str(symbol_data.bid).ljust(10)} {str(symbol_data.ask).ljust(10)}")
        print(f"{symbol_data.name.ljust(8)} {str(symbol_data.last).ljust(10)} {str(symbol_data.session_volume).ljust(12)}")
    # Espera um intervalo antes de verificar novamente (por exemplo, 1 segundo)
    time.sleep(1)

def list_available_symbols():
    # Obtém a lista de todos os símbolos disponíveis
    symbols = mt5.symbols_get()
    # Filtra a lista de símbolos para encontrar os que contêm "VALE"
    vale_symbols = [symbol.name for symbol in symbols if TICKER in symbol.name]
    # Verifica se algum símbolo foi encontrado
    if not vale_symbols:
        print("Nenhum símbolo contendo 'VALE' foi encontrado.")
    else:
        print("Símbolos encontrados:")
        for s in vale_symbols:
            print(s)

# Finaliza a conexão com o terminal MetaTrader 5
mt5.shutdown()
