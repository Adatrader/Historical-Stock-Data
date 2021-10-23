from pandas.core.frame import DataFrame
import yfinance as yf
import pandas


class Stock:
    def __init__(self, ticker, period, interval):
        self.ticker = ticker
        self.period = period
        self.interval = interval
        self.df = DataFrame()

    def get_ticker_data(self):
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        self.df = yf.download(tickers=self.ticker,
                              period=self.period, interval=self.interval)

    # Convert to quantconnect lean formatting
    def convert(self):
        pass

    def export(self):
        self.df.to_csv(
            f'{self.ticker}_{self.interval}_{self.period}.csv', index=False)


if __name__ == "__main__":
    tickers = ["SPY", "DIA", "QQQ"]
    for elem in tickers:
        data = Stock(elem, "max", "1d")
        data.get_ticker_data()
        data.export()
