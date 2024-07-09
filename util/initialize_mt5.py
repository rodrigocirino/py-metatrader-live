import MetaTrader5 as mt5


class MQL5:

    def initialize(self):
        if not mt5.initialize():
            print("initialize() falhou")
            exit()
        return mt5

    def finalize(self):
        mt5.shutdown()
