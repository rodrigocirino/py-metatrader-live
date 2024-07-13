import sched
import time
from datetime import datetime

import pandas as pd
import numpy as np

from util.Rates import Rates

servicemanager = "mt5"


class TickReceiver:

    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        self.df = pd.DataFrame()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.from_date = datetime.now()
        self.rates = Rates(servicemanager)

    def enter_scheduler(self):
        self.scheduler.enter(self.interval, 1, self.load_until_now)
        self.scheduler.run()

    def load_until_now(self):
        # Obter os dados OHLC
        bars = self.rates.rates_from(self.symbol)
        # bars = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M5, 0, num_bars)
        df = pd.DataFrame(bars)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        # Definir a coluna 'time' como índice
        df.set_index('time', inplace=True)
        self.df = df  # populate dataframe
        # SYSOUT
        print(df)
        # Update Scheduler
        self.enter_scheduler()

    def process_ticks(self):
        bars = self.rates.rates_from(self.symbol)
        # bars = self.rates.symbol_info(self.symbol)
        if bars is None:
            print(f"Não foi possível obter informações sobre o símbolo {self.symbol}")
        else:
            self.update_dataframe(bars)
            self.calculate_atr()
            self.is_atr_over()
            self.ema()
            # SYSOUT
            self.print_dataframe()
        # Update Scheduler
        self.enter_scheduler()

    def print_dataframe(self):
        self.df.drop(columns=['tick_volume', 'spread', 'real_volume'], errors='ignore', inplace=True)
        # self.df = self.df.loc[(self.df.index >= pd.Timestamp("2024-07-10 10:15:00"))]
        pd.set_option('display.max_columns', None)  # Ensure all columns are printed
        print(self.df)
        # print("> Barras com ATR 20 Superior a 1.5 vezes.")
        # print(self.df.loc[self.df.is_over].tail(115))
        print((self.df.loc[:, ~self.df.columns.isin(['open', 'high', 'low'])]).tail(40))

    def update_dataframe(self, bars):
        stime = pd.to_datetime(bars.time, unit='s')
        new_record = pd.DataFrame({'close': bars.last}, index=[stime])
        self.df = pd.concat([self.df, new_record])
        self.df = self.df[~self.df.index.duplicated(keep='last')]  # Remove duplicate times, keep the last

    def calculate_atr(self, n=14):
        """Calculates the ATR (Average True Range) for the last n bars."""
        # Wilder quer calcular a amplitude maior, se a minima for mais distante que a maxima do fechamento anterior use esta, senao a outra
        #  ATR = MME(máx(H – L, H – Cp, Cp – L)) - Cp=previous close
        dff = pd.DataFrame()
        dff['H-L'] = self.df['high'] - self.df['low']
        dff['|H-Cp|'] = np.abs(self.df['high'] - self.df['close'].shift(1))
        dff['|L-Cp|'] = np.abs(self.df['low'] - self.df['close'].shift(1))
        dff['TR'] = dff[["|H-Cp|", "H-L", "|L-Cp|"]].max(axis=1)
        # 
        sma = dff['TR'].rolling(window=n, min_periods=n).mean()[:n]
        rest = dff['TR'][n:]
        dff['true_range'] = pd.concat([sma, rest]).ewm(alpha=1 / n, adjust=False).mean()  # Calculate MME
        self.df['true_range'] = dff['true_range'].round(decimals=2)
        # Número máximo de ações permitidas = shares = total_capital * risk / df['ATR'].iloc[-1] # total_capital = 20000, risk = 0.005

    def ema(self, s=20):
        self.df["EMA" + str(s)] = self.df['close'].ewm(span=s).mean().round(decimals=0)

    def is_atr_over(self):
        self.df['is_over'] = abs(self.df['open'] - self.df['close']) > (self.df['true_range'].shift() * 1.5)

    def run(self):
        try:
            if self.rates.initialize():
                self.enter_scheduler()
            else:
                print("Falha na inicialização do serviço.")
        except KeyboardInterrupt:
            print("Interrupção pelo usuário. Encerrando o programa...")
        finally:
            self.rates.finalize()


if __name__ == "__main__":
    tick_receiver = TickReceiver(symbol="WIN$D", interval=3)
    tick_receiver.run()  # infinite loop
