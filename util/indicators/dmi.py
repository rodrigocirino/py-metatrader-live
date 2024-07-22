import pandas_ta as ta

from util.indicators.command import Command


class Dmi(Command):

    def __init__(self, bars):
        self.df = bars
        self.execute()

    def execute(self):
        cut = 27
        df = self.df
        df = ta.adx(df.high, df.low, df.close, length=6, lensig=6, mamode="ema")
        #  ADX_lensig, DMP_length, DMN_length
        self.df["adx_up"] = (df["ADX_6"] > cut) & (df["DMP_6"] > df["DMN_6"]) & (df["DMP_6"] > cut)
        self.df["adx_dw"] = (df["ADX_6"] > cut) & (df["DMP_6"] < df["DMN_6"]) & (df["DMN_6"] > cut)
