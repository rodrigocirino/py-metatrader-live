from datetime import datetime

import pandas as pd
import numpy as np

from service.mt5_service import MT5_Service
from util.indicators.ema import Ema
from util.indicators.true_range import TrueRange
from util.scheduler import scheduler

servicemanager = "mt5"


class TickReceiver:

    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        self.df = pd.DataFrame()
        self.scheduler = scheduler(interval)
        self.from_date = datetime.now()
        self.rates = MT5_Service(servicemanager)

    def print_dataframe(self):
        self.df.drop(columns=['tick_volume', 'spread', 'real_volume'], errors='ignore', inplace=True)
        pd.set_option('display.max_columns', None)  # Ensure all columns are printed
        print((self.df.loc[:, ~self.df.columns.isin(['open', 'high', 'low'])]).tail(40))
        # self.df = self.df.loc[(self.df.index >= pd.Timestamp("2024-07-10 10:15:00"))]
        # print("> Barras com ATR 20 Superior a 1.5 vezes.")
        # print(self.df.loc[self.df.is_over].tail(115))

    def mining_dataframe(self, bars):
        self.df = pd.DataFrame(bars)
        self.df['time'] = pd.to_datetime(self.df['time'], unit='s')
        self.df.set_index('time', inplace=True)

    def process_ticks(self):
        bars = self.rates.rates_from(self.symbol)
        # bars = self.rates.symbol_info(self.symbol)
        if bars is None:
            print(f"Não foi possível obter informações sobre o símbolo {self.symbol}")
        else:
            self.mining_dataframe(bars)

            dtr = TrueRange(self.df)
            dtr.execute()

            dema = Ema(self.df)
            dema.execute()

            # print("\n =========== XXXXXXXXXXXXXXX =================\n")
            self.print_dataframe()
        # Update Scheduler
        self.scheduler.renew(self.process_ticks)

    def run(self):
        try:
            if self.rates.initialize():
                self.scheduler.renew(self.process_ticks())
            else:
                print("Falha na inicialização do serviço.")
        except KeyboardInterrupt:
            print("Interrupção pelo usuário. Encerrando o programa...")
        finally:
            self.rates.finalize()


if __name__ == "__main__":
    tick_receiver = TickReceiver(symbol="EURUSD", interval=5)
    tick_receiver.run()  # infinite loop
