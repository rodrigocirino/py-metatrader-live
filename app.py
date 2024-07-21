import os
from datetime import datetime

import pandas as pd

from service.mt5_service import MT5_Service
from service.scheduler import scheduler
from util.indicators.aroon_oscilator import Aroon
from util.indicators.command import CommandController
from util.indicators.ema import Ema
from util.indicators.true_range import TrueRange

servicemanager = "mt5"


class TickReceiver:

    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        self.df = pd.DataFrame()
        self.scheduler = scheduler(interval)
        self.from_date = datetime.now()
        self.rates = MT5_Service(servicemanager)

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

    def mining_dataframe(self, bars):
        self.df = pd.DataFrame(bars)
        self.df["time"] = pd.to_datetime(self.df["time"], unit="s")
        self.df.set_index("time", inplace=True)

    def process_ticks(self):
        bars = self.rates.rates_from(self.symbol)
        # bars = self.rates.symbol_info(self.symbol)
        if bars is None:
            print(f"Não foi possível obter informações sobre o símbolo {self.symbol}")
        else:
            self.mining_dataframe(bars)

            self.analyze_indicators()

            self.print_dataframe()

            self.recent_dataframe()
        # Update Scheduler
        self.scheduler.renew(self.process_ticks)

    def print_dataframe(self):
        # inplace=True
        print(f"{'> ' * 5} Período disponível: {self.df.index.min()} a {self.df.index.max()}")
        self.df.drop(
            columns=["tick_volume", "spread", "real_volume"],  # "open", "high", "low"
            errors="ignore",
            inplace=True,
        )
        df = self.df[
            (self.df.index >= pd.Timestamp("2024-07-18 00:00:01")) & (self.df.index <= pd.Timestamp("2024-07-18 23:59:59"))
        ]
        df.index = (
            pd.to_datetime(df.index).tz_localize("Etc/GMT-2").tz_convert("Etc/GMT+3")
        )  # Etc/GMT+3, Brazil/East, America/Sao_Paulo
        pd.set_option("display.max_columns", None)  # Ensure all columns are printed
        pd.set_option("display.max_rows", 100)  # Ensure all columns are printed
        print(df)
        # print((self.df.loc[:, ~self.df.columns.isin(["open", "high", "low"])]).tail(100))
        # print(df[["tick_volume"]].sort_values("tick_volume", ascending=False).tail(100))

    def log_to_csv(self):

        log_filepath = "util/export"
        os.makedirs(log_filepath, exist_ok=True)
        self.df.to_csv(f"{log_filepath}/console.csv")  # , sep="\t", decimal=',')

    def recent_dataframe(self):
        df = (self.df.loc[:, ~self.df.columns.isin(["open", "high", "low"])]).tail(100)
        self.log_to_csv()
        print(f"\n{'_' * 65}")
        print(df.iloc[-1:])

    def analyze_indicators(self):
        # Cria uma instância do controlador
        controller = CommandController()
        # Adiciona os comandos ao controlador
        controller.add_command(TrueRange(self.df))
        controller.add_command(Ema(self.df))
        controller.add_command(Aroon(self.df))
        # Processa os comandos
        controller.process_command()


if __name__ == "__main__":
    tick_receiver = TickReceiver(symbol="Bra50", interval=10)
    tick_receiver.run()  # infinite loop

"""
_________________________________________________________________
                       close  atr_1.5 EMA20COLOR aroon_strength
time                                                           
2024-07-19 03:55:00  2425.86    False        Red          Médio
RATES GOLD with mt5
"""
