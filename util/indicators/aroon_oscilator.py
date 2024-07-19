from util.indicators.command import Command
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import pytz
import os


class Aroon(Command):
    def __init__(self, bars):
        self.df = bars

    def execute(self):
        self.aroon()

    def aroon(self):
        # Calcular o Aroon (Aroon Up e Aroon Down) para medir a força da tendência
        aroon = ta.aroon(self.df['high'], self.df['low'], length=14)
        data = pd.DataFrame()
        data['Aroon_Up'] = aroon['AROONU_14']
        data['Aroon_Down'] = aroon['AROOND_14']
        # Aplicar a função define_trend_strength para cada par de valores Aroon Up e Aroon Down e criar uma nova coluna
        data['Trend_Strength'] = data.apply(lambda row: self.define_trend_strength(row['Aroon_Up'], row['Aroon_Down']),
                                            axis=1)
        self.df['aroon_strength'] = data['Trend_Strength']
        # print((self.df.loc[:, ~self.df.columns.isin(['open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume'])]).tail(40))

    def define_trend_strength(self, aroon_up, aroon_down):
        if aroon_up > 80 and aroon_down < 20:
            return "Forte Alta"
        elif aroon_down > 80 and aroon_up < 20:
            return "Forte Baixa"
        elif (50 <= aroon_up <= 80 and aroon_down < 50) or (50 <= aroon_down <= 80 and aroon_up < 50):
            return "Médio"
        else:
            return "Neutro"
