from datetime import datetime

import pandas as pd

from service.loggs import Loggs
from service.mt5_service import MT5_Service
from service.pandas_options import PandasConfig
from service.scheduler import Scheduler
from util.indicators.advice_trading import AdviceTrading
from util.indicators.aroon import Aroon
from util.indicators.command import CommandController
from util.indicators.dmi import Dmi
from util.indicators.ema import Ema
from util.indicators.stochastic import Stochastic
from util.indicators.true_range import TrueRange

PandasConfig.apply_settings()

loggs = Loggs().logger


class TickReceiver:

    def __init__(self, servicemanager, symbols, timeframe):
        self.symbol = symbols
        self.df = pd.DataFrame()
        self.scheduler = Scheduler()
        self.from_date = datetime.now()
        self.servicemanager = servicemanager
        self.rates = MT5_Service(servicemanager, timeframe)

    def mining_dataframe(self, bars):
        self.df = pd.DataFrame(bars)
        if self.df.index.name != "time":  # Set 'time' as index if not already
            self.df.set_index("time", inplace=True)
        self.df.index = pd.to_datetime(self.df.index, unit="s", utc=True)
        # MT5 não traz a info de tz, qual timezone ele esta retornando, calcule manualmente o shift
        if self.servicemanager.startswith("mt5"):
            self.df["zone"] = self.df.index.tz_convert("Etc/GMT+5")
        else:
            self.df["zone"] = self.df.index.tz_convert("America/Sao_Paulo")
        self.df["zone"] = self.df["zone"].dt.strftime("%H:%M:%S")
        # Etc/GMT+3, Brazil/East, America/Sao_Paulo

    def process_ticks(self):
        loggs.info(f"{'.' * 100}\n")
        bars = self.rates.rates_from(self.symbol)
        if bars is None:
            print(f"Não foi possível obter informações sobre o símbolo {self.symbol}")
        else:
            loggs.info(f"-- Rates of {self.symbol} with {self.servicemanager} in {datetime.now()} --")
            self.mining_dataframe(bars)

            self.analyze_indicators()

            self.print_dataframe()

            # self.one_last_dataframe()

            AdviceTrading(self.df)
        # Update Scheduler
        self.scheduler.renew(self.process_ticks)

    def print_dataframe(self):
        self.df.drop(
            columns=["tick_volume", "spread", "real_volume"],  # "open", "high", "low"
            errors="ignore",
            inplace=True,
        )
        df = self.df.loc[:, ~self.df.columns.isin(["close", "open", "high", "low"])]
        loggs.info(f"-- {self.symbol} Período disponível: {df.index.min()} a {df.index.max()}")
        loggs.info(f"\n{'_' * 10} print_dataframe {'_' * 50}")
        loggs.info(df[self.df.index >= pd.Timestamp.now(tz="UTC").normalize()].tail(15).to_string(index=False))
        # print(df[["tick_volume"]].sort_values("tick_volume", ascending=False).tail(100))

    def one_last_dataframe(self):
        df = self.df.loc[:, ~self.df.columns.isin(["open", "high", "low"])]
        loggs.info(f"\n{'_' * 10} one_last_dataframe {'_' * 50}")
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
        controller.add_command(Stochastic(self.df))
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
    service = ["yfinance", "mt5", "mt5", "mt5"]
    symbol = ["^SPX", "GOLD", "MinDolAug24", "HKInd"]
    item = 0
    tick_receiver = TickReceiver(service[item], symbol[item], 5)
    tick_receiver.run()  # run scheduler
