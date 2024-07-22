from datetime import datetime

import pandas as pd

from service.loggs import Loggs
from service.mt5_service import MT5_Service
from service.scheduler import scheduler
from util.indicators.aroon_oscilator import Aroon
from util.indicators.command import CommandController
from util.indicators.ema import Ema
from util.indicators.true_range import TrueRange

loggs = Loggs().logger


class TickReceiver:

    def __init__(self, servicemanager, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        self.df = pd.DataFrame()
        self.scheduler = scheduler(interval)
        self.from_date = datetime.now()
        self.rates = MT5_Service(servicemanager)
        loggs.info("RATES " + str(self.symbol) + " with " + str(servicemanager))

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

    # def config_logger(self): LogSelf(self.symbol).config_logger()

    def mining_dataframe(self, bars):
        self.df = pd.DataFrame(bars)
        self.df["time"] = pd.to_datetime(self.df.index, unit="s")
        self.df.set_index("time", inplace=True)

    def process_ticks(self):
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
        pd.set_option("display.max_columns", None)  # Ensure all columns are printed
        pd.set_option("display.max_rows", 100)  # Ensure all columns are printed
        df = (self.df.loc[:, ~self.df.columns.isin(["open", "high", "low"])]).tail(30)
        loggs.info(f"{'> ' * 3} {self.symbol} Período disponível: {df.index.min()} a {df.index.max()}")
        loggs.info(f"\n---\tprint_dataframe\t{'-' * 65}")
        loggs.info(df)
        """ 
        df = self.df[
            (self.df.index >= pd.Timestamp("2024-07-18 00:00:01")) & (self.df.index <= pd.Timestamp("2024-07-18 23:59:59"))
        ] 
        df.index = (
            pd.to_datetime(df.index).tz_localize("Etc/GMT-2").tz_convert("Etc/GMT+3")
        )  # Etc/GMT+3, Brazil/East, America/Sao_Paulo        
        """
        # logging.info(f"\r\n{'.'*5}\tColunas do Dataframe\t{'.'*5}\n\t[%s]\n", ", ".join(df.columns))
        # print((self.df.loc[:, ~self.df.columns.isin(["open", "high", "low"])]).tail(100))
        # print(df[["tick_volume"]].sort_values("tick_volume", ascending=False).tail(100))

    """
    def log_to_csv(self):
        log_filepath = "./export"
        os.makedirs(log_filepath, exist_ok=True)
        self.df.to_csv(f"{log_filepath}/console.csv")  # , sep="\t", decimal=',')
    """

    def one_last_dataframe(self):
        df = (self.df.loc[:, ~self.df.columns.isin(["open", "high", "low"])]).tail(100)
        loggs.info(f"\n---\tone_last_dataframe\t{'-' * 65}")
        loggs.info(df.iloc[-1:])

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
    service = ["yfinance", "mt5"]
    symbol = ["^SPX", "GOLD"]
    item = 1
    tick_receiver = TickReceiver(servicemanager=service[item], symbol=symbol[item], interval=20)
    # tick_receiver.config_logger()
    tick_receiver.run()  # run scheduler

"""
_________________________________________________________________
                       close  atr_1.5 EMA20COLOR aroon_strength
time                                                           
2024-07-19 03:55:00  2425.86    False        Red          Médio
RATES GOLD with mt5
"""
