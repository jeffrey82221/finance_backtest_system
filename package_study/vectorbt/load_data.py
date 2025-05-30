import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
import datetime as dt

symbol = '0050.TW'

data = yf.Ticker(symbol) 
ts = data.history(start='2021-01-01', end='2025-05-23')
df = pd.DataFrame(ts) 
print(df.columns)

