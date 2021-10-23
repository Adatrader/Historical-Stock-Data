import os
from pandas.core.frame import DataFrame
import yfinance as yf
from equity_lists.SP500 import ticker_list
from zipfile import ZipFile
from os import path


class Stock:
    def __init__(self, ticker, period, interval):
        self.ticker = ticker
        self.period = period
        self.interval = interval
        self.df = DataFrame()

    def get_ticker_data(self):
        """
        Yahoo finance data feed
        Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        """
        self.df = yf.download(tickers=self.ticker,
                              period=self.period, interval=self.interval)
        self.df.reset_index(inplace=True)

    def convert(self):
        """
        Convert datasets to quantconnect standard format
        Datetime: YYYYMMDD HH:MM
        Deci-cents
        """
        # Reformat date to quantconnect format
        _df = self.df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        try:
            _df['Date'] = _df['Date'].map(str)
            _df['Date'] = _df['Date'].str.replace(r'-|/', '')
            _df['Date'] = [x[:-3] for x in _df['Date']]
        except:
            print("Failed to map date for:" + str(self.ticker))

        # Deci-cents conversion (10,000 * dollars)
        columns = ['Open', 'High', 'Low', 'Close']
        try:
            for col in columns:
                _df[col] = _df[col] * 10000
                _df[col] = _df[col].map(int)
        except:
            print("Failed to map to deci-cents for: " + str(self.ticker))
        self.df = _df

    def export(self):
        """
        Store in correct sub-directory for interval
        Save as [ticker].csv
        Zip csv and remove residual
        """
        interval = self.interval
        if self.interval == "1d":
            interval = "daily"
        filename = f'{self.ticker.lower()}.csv'
        self.df.to_csv(
            filename, index=False, header=None)

        if path.exists(filename):
            src = path.realpath(filename)

        # zipfile
        if src is not None:
            with ZipFile(f'data/{interval}/{self.ticker.lower()}.zip', "w") as newzip:
                newzip.write(filename)

        # Remove csv after compress
        os.remove(f'{self.ticker.lower()}.csv')


if __name__ == "__main__":
    # Ticker list is currently s&p500 stocks
    for ticker in ticker_list.keys():
        print("Getting data for ticker:" + str(ticker))
        data = Stock(ticker, "max", "1d")
        data.get_ticker_data()
        data.convert()
        data.export()
