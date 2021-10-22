import yfinance as yf


def getTickerData(symbol, timeframe):
    df = yf.download(symbol)
    print(df)
