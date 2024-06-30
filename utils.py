import yfinance as yf
import pandas as pd

def download_data(ticker, start_date="2015-01-01"):
    data = yf.download(ticker, start=start_date)
    data.index = pd.to_datetime(data.index)
    data = data.asfreq('B')  # 'B' indicates business days
    data = data.ffill().dropna()  # Forward fill NaN values and drop remaining NaNs
    return data