from service.loggs import Loggs
from service.pandas_options import PandasConfig

PandasConfig.apply_settings()

loggs = Loggs().logger


class AdviceTrading:

    def __init__(self, bars):
        self.df = bars
        self.advices_trading()

    def advices_trading(self):
        last_row = self.df.iloc[-1]
        loggs.info(f"\n{'_' * 10} advices_trading {'_' * 50}")

        if last_row.ema20:
            loggs.info(f"{last_row.ema20.upper().ljust(10)} - EMA20")
            print(f"... direcional de médias não indica entradas")

        if last_row.afs:
            loggs.info(f"AFASTAMENTO ALTO - mais que 0.25% distante da EMA20")
            print(f"... STOP abaixo da mínima/máxima anterior")

        if last_row.atrs:
            loggs.info(f"ATR Climax - Não sei oque fazer aqui, aguarde!")
            print(f"... Entradas em 50% da barra, Stop máximo no comprimento da barra")

        if last_row.aroon:
            loggs.info(f"{last_row.aroon.upper().ljust(10)} - AROON - Tendência ativada")
            # print(f"...")

        if last_row.adx_up:
            loggs.info(f"ALTISTA com ADX/DI+ - Tendência forte de alta")
            print(f"... Cuidado com sobrecompras e sobrevendas!!, Se reverter saia rapidamente.")

        if last_row.adx_dw:
            loggs.info(f"BAIXISTA com ADX/DI- - Tendência forte de baixa")
            # print(f"...")
