from util.indicators.command import Command


class Ema(Command):
    def __init__(self, bars):
        self.df = bars

    def execute(self):
        self.ema()

    def ema(self, s=20):
        self.df["EMA" + str(s)] = self.df['close'].ewm(span=s).mean()  # .round(decimals=0)
