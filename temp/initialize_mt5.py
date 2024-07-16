import MetaTrader5 as mt5


class MQL5:

    @staticmethod
    def initialize():
        if not mt5.initialize():
            print("initialize() fail")
            exit()
        return mt5

    @staticmethod
    def finalize():
        mt5.shutdown()
