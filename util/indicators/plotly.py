import mplfinance as mpf
import pandas as pd
import pandas_ta as ta
import yfinance as yf

"""
ticker = "^GSPC"
df = yf.download(ticker, period="5d", interval=f"5m")
backDays = pd.Timedelta(days=1)  # today + x days
data = df[df.index >= (pd.Timestamp.now(tz="UTC").normalize() - backDays)]
rsi = ta.rsi(data["Close"])
ema = ta.ema(data["Close"])
timeperiod = 6
adx = ta.adx(data["High"], data["Low"], data["Close"], length=timeperiod, lensig=timeperiod, mamode="ema", inplace=True)
apds = [
    mpf.make_addplot(ema, color="blue", panel=0, secondary_y=False, linestyle="dashed"),
    mpf.make_addplot(rsi, panel=1, color="purple", ylabel="RSI"),
    mpf.make_addplot(adx[adx.columns[0]], panel=2, color="yellow", ylabel="ADX", type="bar", alpha=0.9),
    mpf.make_addplot(adx[adx.columns[1]], panel=2, color="blue", linewidths=3),
    mpf.make_addplot(adx[adx.columns[2]], panel=2, color="lime"),
]
mpf.plot(
    data,
    type="candle",
    addplot=apds,
    fontscale=0.65,
    figsize=(12, 8),
    tight_layout=True,
    title=f"{ticker} - {data.index.min()} a {data.index.max()}",
)
"""


class StockPlotter:
    def __init__(self, ticker, period="5d", interval="5m"):
        self.ticker = ticker
        self.data = yf.download(ticker, period=period, interval=interval)

    def plot(self, backDays=1, **kwargs):
        # Filtrar dados dos últimos backDays dias
        data = self.data[self.data.index >= (pd.Timestamp.now(tz="UTC").normalize() - pd.Timedelta(days=backDays))]

        apds = []
        for indicator, params in kwargs.items():
            if indicator == "rsi":
                rsi = ta.RSI(data["Close"], timeperiod=params.get("timeperiod", 14))
                apds.append(
                    mpf.make_addplot(
                        rsi, panel=params.get("panel", 1), color=params.get("color", "purple"), ylabel="RSI"
                    )
                )
            elif indicator == "ema":
                ema = ta.EMA(data["Close"], timeperiod=params.get("timeperiod", 20))
                apds.append(
                    mpf.make_addplot(
                        ema,
                        panel=params.get("panel", 0),
                        color=params.get("color", "blue"),
                        secondary_y=params.get("secondary_y", False),
                        linestyle=params.get("linestyle", "dashed"),
                    )
                )
            elif indicator == "adx":
                timeperiod = params.get("timeperiod", 14)
                adx = ta.ADX(data["High"], data["Low"], data["Close"], timeperiod=timeperiod)
                apds.append(
                    mpf.make_addplot(
                        adx,
                        panel=params.get("panel", 2),
                        color=params.get("color", "yellow"),
                        ylabel="ADX",
                        type=params.get("type", "bar"),
                        alpha=params.get("alpha", 0.9),
                    )
                )

        # Plotar o gráfico
        mpf.plot(
            data,
            type="candle",
            addplot=apds,
            fontscale=0.65,
            figsize=(12, 8),
            tight_layout=True,
            title=f"{self.ticker} - {data.index.min()} a {data.index.max()}",
        )


# Exemplo de uso
ticker = "^GSPC"
plotter = StockPlotter(ticker)
plotter.plot(
    backDays=1,
    rsi={"timeperiod": 14, "panel": 1, "color": "purple"},
    ema={"timeperiod": 20, "panel": 0, "color": "blue", "secondary_y": False, "linestyle": "dashed"},
    adx={"timeperiod": 14, "panel": 2, "color": "yellow", "type": "bar", "alpha": 0.9},
)
