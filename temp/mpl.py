import mplfinance as mpf
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# Baixar dados do S&P 500 (^GSPC)
ticker = "GC=F"
df = yf.download(ticker, period="5d", interval=f"5m")
# Show only today
backDays = pd.Timedelta(days=1)  # today + x days
data = df[df.index >= (pd.Timestamp.now(tz="UTC").normalize() - backDays)]

# Calcular o RSI
rsi = ta.rsi(data["Close"])

# Calcular a EMA de 20 períodos
ema = ta.ema(data["Close"])

# Calcular o DMI
timeperiod = 6
adx = ta.adx(data["High"], data["Low"], data["Close"], length=timeperiod, lensig=timeperiod, mamode="ema", inplace=True)

# Preparar os gráficos adicionais
apds = [
    mpf.make_addplot(ema, color="blue", panel=0, secondary_y=False, linestyle="dashed"),
    mpf.make_addplot(rsi, panel=1, color="purple", ylabel="RSI"),
    mpf.make_addplot(adx[adx.columns[0]], panel=2, color="yellow", ylabel="ADX", type="bar", alpha=0.9),
    mpf.make_addplot(adx[adx.columns[1]], panel=2, color="blue", linewidths=3),
    mpf.make_addplot(adx[adx.columns[2]], panel=2, color="lime"),
]

# Configurar e plotar o gráfico
mpf.plot(
    data,
    type="candle",
    style="yahoo",
    addplot=apds,
    fontscale=0.7,
    figsize=(16, 8),
    # tight_layout=True,
    volume=True,
    title=f"{ticker} - {data.index.min()} a {data.index.max()}",
    savefig="plot.png",
)
