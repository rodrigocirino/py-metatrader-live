import numpy as np
import pandas as pd

from util.indicators.command import Command


class TrueRange(Command):
    def __init__(self, bars):
        self.df = bars

    def execute(self):
        self.calculate_atr()

    def calculate_atr(self, n=14):
        """Calculates the ATR (Average True Range) for the last n bars."""
        # Wilder quer calcular a amplitude maior, se a minima for mais distante que a maxima do fechamento anterior use esta, senao a outra
        #  ATR = MME(máx(H – L, H – Cp, Cp – L)) - Cp=previous close
        dff = self.df.copy()  # pd.DataFrame()
        dff['H-L'] = self.df['high'] - self.df['low']
        dff['|H-Cp|'] = np.abs(self.df['high'] - self.df['close'].shift(1))
        dff['|L-Cp|'] = np.abs(self.df['low'] - self.df['close'].shift(1))
        dff['TR'] = dff[["|H-Cp|", "H-L", "|L-Cp|"]].max(axis=1)
        #
        sma = dff['TR'].rolling(window=n, min_periods=n).mean()[:n]
        rest = dff['TR'][n:]
        dff['true_range'] = pd.concat([sma, rest]).ewm(alpha=1 / n, adjust=False).mean()  # Calculate MME
        # Número máximo de ações permitidas = shares = total_capital * risk / df['ATR'].iloc[-1] # total_capital = 20000, risk = 0.005

        self.is_atr_over(dff['true_range'])

    def is_atr_over(self, true_range):
        mult = 1.50
        self.df['atr_' + str(mult)] = abs(self.df['open'] - self.df['close']) > (true_range.shift() * mult)
