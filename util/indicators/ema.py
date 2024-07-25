from util.indicators.command import Command

"""
Confict with Sideways Alert: Se a EMA esta muito proxima, cruzando ou tem um alerta de mercado lateral
devemos operar contra a media movel, não a favor.
"""


class Ema(Command):
    def __init__(self, bars):
        self.df = bars

    def execute(self):
        self.ema()
        self.afastamento()

    def ema(self, s=20):
        ema = self.df["close"].ewm(span=s).mean()
        color_column = "ema" + str(s)
        self.df[color_column] = ""  # Default color
        self.df.loc[self.df["low"] > ema, color_column] = "Altista"
        self.df.loc[self.df["high"] < ema, color_column] = "Baixista"

    def afastamento(self, s=20):
        ema = self.df["close"].ewm(span=s).mean()
        afs_ema20 = (self.df["close"] - ema) / ema * 100
        self.df["afs"] = abs(afs_ema20) > 0.20
