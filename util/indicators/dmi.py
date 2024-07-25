import pandas_ta as ta

from util.indicators.command import Command


class Dmi(Command):

    def __init__(self, bars):
        self.df = bars
        self.execute()

    def execute(self):
        cut_adx = 25
        cut_di = 25
        dmi = ta.adx(self.df.high, self.df.low, self.df.close, length=12, lensig=12, mamode="ema")
        if dmi is not None:
            adx, diplus, diminus = dmi.columns
            dmi.rename(columns={adx: "ADX", diplus: "DP", diminus: "DM"}, inplace=True)
            #  ADX_lensig, DMP_length, DMN_length
            self.df["adx_up"] = (dmi["ADX"] >= cut_adx) & (dmi["DP"] > dmi["DM"]) & (dmi["DP"] >= cut_di)
            self.df["adx_dw"] = (dmi["ADX"] >= cut_adx) & (dmi["DP"] < dmi["DM"]) & (dmi["DM"] >= cut_di)
