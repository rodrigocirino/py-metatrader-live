import sched
import time
from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd


class TickReceiver:
    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.from_date = datetime.now()

    def initialize(self):
        if not mt5.initialize():
            print("initialize() falhou")
            exit()

    def create_scheduler(self):
        self.scheduler.enter(self.interval, 1, self.load_until_now)

    def load_until_now(self):
        num_bars = 10000  # número de barras de dados para recuperar
        # Obter os dados OHLC
        bars = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M5, 0, num_bars)
        df = pd.DataFrame(bars)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        # Definir a coluna 'time' como índice
        df.set_index('time', inplace=True)
        print(df)
        # RENEW SCHEDULER
        self.scheduler.enter(self.interval, 1, self.load_until_now)

    def finalize(self):
        mt5.shutdown()

    def run(self):
        try:
            self.create_scheduler()
            self.scheduler.run()
        except KeyboardInterrupt:
            print("Interrupção pelo usuário. Encerrando o programa...")
        finally:
            self.finalize()

# Exemplo de uso
if __name__ == "__main__":
    INTERVAL = 5*60
    TICKER = "VALE3"
    print(f"Updating {TICKER} every {INTERVAL} sec.")
    tick_receiver = TickReceiver(TICKER, INTERVAL)
    tick_receiver.initialize()
    tick_receiver.load_until_now()
    tick_receiver.run()
