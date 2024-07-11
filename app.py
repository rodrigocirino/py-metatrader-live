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
        num_bars = 1000  # número de barras de dados para recuperar
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
            self.is_atr_over()
            # SYSOUT
            self.print_dataframe()
        self.scheduler.enter(self.interval, 1, self.process_ticks)

    def print_dataframe(self):
        self.df.drop(columns=['tick_volume', 'spread', 'real_volume'], errors='ignore', inplace=True)
        # self.df = self.df.loc[(self.df.index >= pd.Timestamp("2024-07-10 10:15:00"))]
        pd.set_option('display.max_columns', None)  # Ensure all columns are printed
        print(self.df)
        print("> Barras com ATR 20 Superior a 1.5 vezes.")
        print(self.df.loc[self.df.is_over].tail(115))

    def update_dataframe(self, symbol_data):
        stime = pd.to_datetime(symbol_data.time, unit='s')
        new_record = pd.DataFrame({'close': symbol_data.last}, index=[stime])
        self.df = pd.concat([self.df, new_record])
        self.df = self.df[~self.df.index.duplicated(keep='last')]  # Remove duplicate times, keep the last

    def calculate_atr(self):
        """Calculates the ATR (Average True Range) for the last 20 bars."""
        dff = pd.DataFrame()
        dff['High-Low'] = self.df['high'] - self.df['low']
        dff['High-PreviousClose'] = abs(self.df['high'] - self.df['close'].shift(1))
        dff['Low-PreviousClose'] = abs(self.df['low'] - self.df['close'].shift(1))
        dff['TrueRange'] = dff[['High-Low', 'High-PreviousClose', 'Low-PreviousClose']].max(axis=1)
        self.df['true_range'] = dff['TrueRange'].rolling(window=20).mean()

    def is_atr_over(self):
        self.df['is_over'] = abs(self.df['open'] - self.df['close']) > (self.df['true_range'].shift() * 1.5)

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
