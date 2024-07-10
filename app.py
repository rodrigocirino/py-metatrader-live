import sched
import time
from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd


class TickReceiver:
    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        self.df = pd.DataFrame()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.from_date = datetime.now()

    @staticmethod
    def initialize():
        if not mt5.initialize():
            print("initialize() falhou")
            exit()

    def create_scheduler(self):
        self.scheduler.enter(self.interval, 1, self.process_ticks)

    def load_until_now(self):
        num_bars = 130  # número de barras de dados para recuperar
        # Obter os dados OHLC
        bars = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M5, 0, num_bars)
        df = pd.DataFrame(bars)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        # Definir a coluna 'time' como índice
        df.set_index('time', inplace=True)
        print(df[['open','high','low','close','tick_volume']])
        self.df = df



    def process_ticks(self):
        symbol_data = mt5.symbol_info(self.symbol)
        # print(
        #    f"{str(pd.to_datetime(symbol_data.time, unit='s')).ljust(20)} {symbol_data.name.ljust(8)}\
        #        {str(symbol_data.last).ljust(10)} {str(symbol_data.session_volume).ljust(12)}")
        if symbol_data is None:
            print(f"Não foi possível obter informações sobre o símbolo {self.symbol}")
        else:
            self.update_dataframe(symbol_data)
        self.scheduler.enter(self.interval, 1, self.process_ticks)

    def update_dataframe(self, symbol_data):
        stime = pd.to_datetime(symbol_data.time, unit='s')
        new_record = pd.DataFrame({'close': symbol_data.last}, index=[stime])
        self.df = pd.concat([self.df, new_record])
        print(self.df[['open', 'high', 'low', 'close', 'tick_volume']])


    @staticmethod
    def finalize():
        mt5.shutdown()

    def run(self):
        try:
            self.create_scheduler()
            self.scheduler.run()
        except KeyboardInterrupt:
            print("Interrupção pelo usuário. Encerrando o programa...")
        finally:
            self.finalize()


if __name__ == "__main__":
    tick_receiver = TickReceiver(symbol="WIN$D", interval=3)
    tick_receiver.initialize()
    tick_receiver.load_until_now()
    print(f"{'Time'.ljust(20)} {'Ticker'.ljust(8)} {'Last'.ljust(10)} {'Volume'.ljust(12)}".upper())
    tick_receiver.run()

# df.columns
# Index(['open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume'], dtype='object')