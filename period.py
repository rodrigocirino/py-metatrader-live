import MetaTrader5 as mt5
import pandas as pd

from util.initialize_mt5 import MQL5
from util.scheduler import Scheduler


class TickReceiver:
    def __init__(self, symbol, interval):
        self.symbol = symbol
        # Init Scheduler
        self.scheduler = Scheduler(interval)
        # Init MQL5 Connection
        MQL5().initialize();

    def run_scheduler(self):
        try:
            self.scheduler.create_scheduler(self.get_data)
        except KeyboardInterrupt:
            print("Interrupção pelo usuário. Encerrando o programa...")
        finally:
            # Init MQL5 Connection
            MQL5().finalize();

    def get_data(self):
        num_bars = 1000  # número de barras de dados para recuperar
        # Obter os dados OHLC
        bars = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M5, 0, num_bars)
        df = pd.DataFrame(bars)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        # Definir a coluna 'time' como índice
        df.set_index('time', inplace=True)
        print(df)
        # RENEW SCHEDULER
        self.run_scheduler()


if __name__ == "__main__":
    INTERVAL = 2 # 5*60
    TICKER = "WIN$D"
    print(f"Updating {TICKER} every {INTERVAL} sec.")
    tick_receiver = TickReceiver(TICKER, INTERVAL)
    tick_receiver.get_data()
