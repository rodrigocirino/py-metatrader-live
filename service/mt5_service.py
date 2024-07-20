import MetaTrader5 as mt5


class MT5_Service:

    def __init__(self, service):
        self.service = service
        self.mt5 = mt5 if (service == "mt5" or service == "mt5_ticks") else None

    def rates_from(self, symbol, num_bars=500):
        print("RATES " + str(symbol) + " with " + str(self.service))
        if self.service == "mt5":
            return mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, num_bars)
        if self.service == "mt5_ticks":
            return mt5.symbol_info(symbol)

    def initialize(self):
        print("SELF SERVICE " + self.service)
        if self.mt5 is not None:
            if not self.mt5.initialize():
                print(
                    "Failed to initialize MetaTrader 5, error code =",
                    self.mt5.last_error(),
                )
                self.mt5.shutdown()
                return False
            else:
                print("MetaTrader 5 initialized successfully")
                return True
        else:
            print("Service not supported")
            return False

    def finalize(self):
        if self.service == "mt5":
            mt5.shutdown()
