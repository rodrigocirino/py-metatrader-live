import pandas_ta as ta

from util.indicators.command import Command

"""Indicator: Stochastic Oscillator (STOCH)"""


class Stochastic(Command):

    def __init__(self, bars):
        self.df = bars
        self.execute()

    def execute(self):
        """
        # Using default params
        k (int): The Fast %K period. Default: 14
        d (int): The Slow %K period. Default: 3
        smooth_k (int): The Slow %D period. Default: 3
        mamode (str): See ```help(ta.ma)```. Default: 'sma'
        """
        stoch = ta.stoch(self.df.high, self.df.low, self.df.close)
        # Renomeando as colunas para nomes mais simples
        if stoch is not None:
            k_name, d_name = stoch.columns
            stoch.rename(columns={k_name: "stoch_k", d_name: "stoch_d"}, inplace=True)
            self.df["stoch_k"] = stoch["stoch_k"].apply(lambda x: round(x, 2))
            self.df["stoch_d"] = stoch["stoch_d"].round(2)

            """
            zscore = ta.zscore(self.df.close, length=20)
            print(zscore)
            stochrsi = ta.stochrsi(self.df.close)
            print(stochrsi)
            """
