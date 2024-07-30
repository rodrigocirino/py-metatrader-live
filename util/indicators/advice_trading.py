from colorist import Color, effect_blink, bg_hex
from flask import Flask

from service.loggs import Loggs

app = Flask(__name__)


class AdviceTrading:

    def __init__(self, bars):
        self.df = bars
        self.advices_trading()

    def advices_trading(self):
        # initialize logs service
        loggs = Loggs().logger

        last_row = self.df.iloc[-1]

        loggs.info(f"\n{'_' * 10} advices_trading {last_row.zone} {'_' * 50}")

        if last_row.close > last_row.open:
            loggs.info(f"{Color.GREEN}Barra de alta{Color.OFF}")

        if last_row.close < last_row.open:
            loggs.info(f"{Color.RED}Barra de baixa{Color.OFF}")

        if last_row.ema20:
            loggs.info(f"{last_row.ema20.upper().ljust(10)} - EMA20")

        if last_row.afs:
            loggs.info(
                f"{effect_blink('AFASTAMENTO ALTO!', Color.YELLOW)}"
                f"\t - mais que 0.2% distante da EMA20 <---- {Color.YELLOW}EVITE ENTRADAS{Color.OFF}"
            )

        if last_row.aroon:
            loggs.info(f"AROON {last_row.aroon.upper().ljust(10)}")
            print(f"... [posicionado] Cuidado com sobrecompras e sobrevendas!!, Se reverter saia rapidamente.")

        if last_row.stoch:
            loggs.info(f"Stochastic {last_row.stoch.upper().ljust(10)}.")

        if last_row.atrs:
            loggs.info(f"{bg_hex('ATR Climax - Não entre a mercado.', '#ffff99')}")
            if last_row.close > last_row.open:
                loggs.info(
                    f"\tBarra de Alta, NÃO VENDA CONTRA, olhe o gráfico! <------- {Color.GREEN}COMPRE NÃO"
                    f" VENDA{Color.OFF}"
                )
            else:
                loggs.info(
                    f"\tBarra de Baixa, NÃO COMPRE CONTRA, olhe o gráfico! <------- {Color.RED}VENDA NÃO"
                    f" COMPRE{Color.OFF}"
                )
            print(f"... [entradas] Entradas em 50% da barra, Stop máximo no comprimento da barra")

        return last_row


"""
from colorist import hex, bg_hex, effect_blink

hex("I want this text in coral Hex colors", "#ff7f50")
bg_hex("I want this background in coral Hex colors", "#ff7f50")
effect_blink("CYAN and BLINKING!", Color.CYAN)
"""

"""
import mplfinance as mpf
mpf.plot(
self.df.tail(150),
type="candle",
style="yahoo",
fontscale=0.8,
figsize=(14, 7),
tight_layout=False,
ema=20,
)
"""
