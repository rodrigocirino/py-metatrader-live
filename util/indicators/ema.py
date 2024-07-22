import pandas as pd

from util.indicators.command import Command

"""
Confict with Sideways Alert: Se a EMA esta muito proxima, cruzando ou tem um alerta de mercado lateral
devemos operar contra a media movel, não a favor.
"""


class Ema(Command):
    def __init__(self, bars):
        self.df = bars
        self.column = None

    def execute(self):
        self.ema()
        self.afastamento()

    def ema(self, s=20):
        data = pd.DataFrame()
        data["EMA"] = self.df["close"].ewm(span=s).mean()
        self.column = "ema" + str(s)
        self.df[self.column] = data["EMA"]  # df['ema20']
        color_column = self.column + "color"
        self.df[color_column] = "White"  # Default color
        self.df.loc[self.df["high"] < data["EMA"], color_column] = "Red"
        self.df.loc[self.df["low"] > data["EMA"], color_column] = "Green"

    def afastamento(self):
        self.df["afs_ema20"] = (self.df["close"] - self.df[self.column].astype(float)) / self.df[self.column].astype(float) * 100
        self.df["afs"] = self.df["afs_ema20"] > 0.25
