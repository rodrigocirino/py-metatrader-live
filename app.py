from datetime import datetime

import pandas as pd

from service.loggs import Loggs
from service.mt5_service import MT5_Service
from service.pandas_options import PandasConfig
from service.scheduler import scheduler
from util.indicators.aroon_oscilator import Aroon
from util.indicators.command import CommandController
from util.indicators.dmi import Dmi
from util.indicators.ema import Ema
from util.indicators.true_range import TrueRange

PandasConfig.apply_settings()

loggs = Loggs().logger


class TickReceiver:

    def __init__(self, servicemanager, symbols, interval):
        self.symbol = symbols
        self.interval = interval
        self.df = pd.DataFrame()
        self.scheduler = scheduler(interval)
        self.from_date = datetime.now()
        self.servicemanager = servicemanager
        self.rates = MT5_Service(servicemanager)
        loggs.info("RATES " + str(self.symbol) + " with " + str(servicemanager))

    def mining_dataframe(self, bars):
        self.df = pd.DataFrame(bars)
        if self.df.index.name != "time":  # Set 'time' as index if not already
            self.df.set_index("time", inplace=True)
        self.df.index = pd.to_datetime(self.df.index, unit="s", utc=True)
        # MT5 não traz qual timestamp ele esta retornando a hora GMT, verifique na plataforma.
        if self.servicemanager.startswith("mt5"):
            self.df["zone"] = self.df.index.tz_convert("Etc/GMT+5")
        else:
            self.df["zone"] = self.df.index.tz_convert("America/Sao_Paulo")
        self.df["zone"] = self.df["zone"].dt.strftime("%H:%M:%S")
        # Etc/GMT+3, Brazil/East, America/Sao_Paulo

    def process_ticks(self):
        loggs.info(f"\n\n{'.' * 100}\n")
        bars = self.rates.rates_from(self.symbol)
        if bars is None:
            print(f"Não foi possível obter informações sobre o símbolo {self.symbol}")
        else:
            self.mining_dataframe(bars)

            self.analyze_indicators()

            self.print_dataframe()

            self.one_last_dataframe()
        # Update Scheduler
        self.scheduler.renew(self.process_ticks)

    def print_dataframe(self):
        self.df.drop(
            columns=["tick_volume", "spread", "real_volume"],  # "open", "high", "low"
            errors="ignore",
            inplace=True,
        )
        df = (self.df.loc[:, ~self.df.columns.isin(["open", "high", "low"])]).tail(30)
        print(f"{'> ' * 3} {self.symbol} Período disponível: {df.index.min()} a {df.index.max()}")
        loggs.info(f"\n---\tprint_dataframe\t{'-' * 65}")
        loggs.info(df)
        """ df[(self.df.index >= pd.Timestamp("2024-07-18 00:00:01")) & (self.df.index <= ...)] """
        # logging.info(f"\r\n{'.'*5}\tColunas do Dataframe\t{'.'*5}\n\t[%s]\n", ", ".join(df.columns))
        # print((self.df.loc[:, ~self.df.columns.isin(["open", "high", "low"])]).tail(100))
        # print(df[["tick_volume"]].sort_values("tick_volume", ascending=False).tail(100))

    def one_last_dataframe(self):
        df = (self.df.loc[:, ~self.df.columns.isin(["open", "high", "low"])]).tail(100)
        loggs.info(f"\n---\tone_last_dataframe\t{'-' * 65}")
        last_row = df.iloc[-1]
        # Imprime cada coluna com seu valor na última linha, alinhando com 50 caracteres de forma pythonica
        loggs.info("\n".join(f"{col.ljust(20)}: {val}" for col, val in df.iloc[-1].items()))

    def analyze_indicators(self):
        # Cria uma instância do controlador
        controller = CommandController()
        # Adiciona os comandos ao controlador
        controller.add_command(TrueRange(self.df))
        controller.add_command(Ema(self.df))
        controller.add_command(Aroon(self.df))
        controller.add_command(Dmi(self.df))
        # Processa os comandos
        controller.process_command()

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
    service = ["yfinance", "mt5", "mt5"]
    symbol = ["^SPX", "GOLD", "MinDolAug24"]
    item = 2
    tick_receiver = TickReceiver(servicemanager=service[item], symbols=symbol[item], interval=30)
    tick_receiver.run()  # run scheduler

"""
__________________________________________________________________________________________________________________
                            close   ADX_UP  ADX_DW  atr_1.5 ema20   ema20color  afs_ema20   afs     aroon_strength
time                                                                           
2024-07-22 14:25:00-04:00   5567    False   False   False   5560    Green       0.134674    False   Forte Alta 
__________________________________________________________________________________________________________________
"""
