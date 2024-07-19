import pandas as pd

from util.indicators.command import Command


class Ema(Command):
    def __init__(self, bars):
        self.df = bars

    def execute(self):
        self.ema()

    def ema(self, s=20):
        data = pd.DataFrame()
        data["EMA"] = self.df["close"].ewm(span=s).mean()  # .round(decimals=0)
        new_column = "EMA" + str(s) + "COLOR"
        self.df[new_column] = "White"  # Default color
        self.df.loc[self.df["high"] < data["EMA"], new_column] = "Red"
        self.df.loc[self.df["low"] > data["EMA"], new_column] = "Green"
