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
        num_bars = 114  # número de barras de dados para recuperar
        # Obter os dados OHLC
        bars = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M5, 0, num_bars)
        df = pd.DataFrame(bars)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        # Definir a coluna 'time' como índice
        df.set_index('time', inplace=True)
        self.df = df  # populate dataframe

    def process_ticks(self):
        symbol_data = mt5.symbol_info(self.symbol)
        if symbol_data is None:
            print(f"Não foi possível obter informações sobre o símbolo {self.symbol}")
        else:
            # PROCESS
            self.update_dataframe(symbol_data)
            self.calculate_atr()
            # SYSOUT
            self.print_dataframe()
        self.scheduler.enter(self.interval, 1, self.process_ticks)

    def print_dataframe(self):
        # print(self.df.columns)
        self.df.drop(columns=['tick_volume', 'spread', 'real_volume'], errors='ignore', inplace=True)
        # self.df = self.df.loc[(self.df.index >= pd.Timestamp("2024-07-10 10:15:00"))]
        pd.set_option('display.max_columns', None)  # Ensure all columns are printed
        print(self.df.head(60))

    def update_dataframe(self, symbol_data):
        stime = pd.to_datetime(symbol_data.time, unit='s')
        new_record = pd.DataFrame({'close': symbol_data.last}, index=[stime])
        self.df = pd.concat([self.df, new_record])
        self.df = self.df[~self.df.index.duplicated(keep='last')]  # Remove duplicate times, keep the last

    def calculate_atr(self):
        """Calculates the ATR (Average True Range) for the last 20 bars."""
        '''
        self.df['atr'] = abs(self.df['open'] - self.df['close'])
        self.df['atr'].rolling(window=20).mean()
        self.df['atr_i'] = self.df['atr'].shift()
        self.df['atr_b'] = self.df['atr'] > self.df['atr_i'] * 2
        self.df.drop(columns=['atr_i'], errors='ignore', inplace=True)
        print(self.df.loc[self.df.atr_b].head(60))
        '''
        """Calculates the ATR (Average True Range) for the last 20 bars."""
        self.df['High-Low'] = self.df['high'] - self.df['low']
        self.df['High-PreviousClose'] = abs(self.df['high'] - self.df['close'].shift(1))
        self.df['Low-PreviousClose'] = abs(self.df['low'] - self.df['close'].shift(1))

        self.df['TrueRange__'] = self.df[['High-Low', 'High-PreviousClose', 'Low-PreviousClose']].max(axis=1)
        self.df['true_range'] = self.df['TrueRange__'].rolling(window=20).mean()
        self.df.drop(columns=['High-Low', 'High-PreviousClose', 'Low-PreviousClose', 'TrueRange__'],
                               errors='ignore', inplace=True)

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
    tick_receiver.run()  # infinite loop
