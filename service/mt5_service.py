import MetaTrader5 as mt5
import yfinance as yf


class MT5_Service:

    def __init__(self, service, timeframe):
        self.service = service
        self.timeframe = timeframe  # in minutes
        self.mt5 = mt5 if (service == "mt5" or service == "mt5_ticks") else None

    def rates_from(self, symbol, num_bars=250):
        # MetaTrader 5 stores tick and bar open time in "Etc/UTC" zone (without the shift)
        if self.service == "mt5":
            return mt5.copy_rates_from_pos(symbol, self.timeframe, 0, num_bars)
        if self.service == "mt5_ticks":
            return mt5.symbol_info(symbol)
        if self.service == "yf":
            return self.online_yf_intraday([symbol])

    def online_yf_intraday(self, stocks):
        # timeframe = interval valid 1m,2m,5m,15m,30m,60m,90m,1h
        # stocks = [stock + ".SA" if not stock.endswith(".SA") and "^" not in stock else stock for stock in stocks]
        df = yf.download(stocks, period="2d", interval=f"{self.timeframe }m")
        df.drop(["Close", "Volume"], axis=1, inplace=True)
        df.index.names = ["time"]  # rename index
        df.rename(columns={"Open": "open", "High": "high", "Low": "low", "Adj Close": "close"}, inplace=True)
        return df

    """
    def on_off_yfinance(self, stocks=None, start=None, end=None, interval="5m", period="60d"):
        # Download percent change
        if stocks is None:
            stocks = []
        # Add ".SA" sufix to Yfinance if the string doesn't end with ".SA" and doesn't contain "^"
        stocks = [stock + ".SA" if not stock.endswith(".SA") and "^" not in stock else stock for stock in stocks]
        data = yf.download(stocks, start=start, end=end, period=period, interval=interval)
        data.index = pd.to_datetime(data.index).tz_convert("Etc/GMT+3")
        return data
    """

    def initialize(self):
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
        elif self.service == "yf":
            print("Yfinance initializing.....")
            return True
        else:
            print("Service not supported")
            return False

    def finalize(self):
        if self.service == "mt5":
            mt5.shutdown()
