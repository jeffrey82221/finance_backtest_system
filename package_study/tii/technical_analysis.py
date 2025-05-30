import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
import datetime as dt

symbol = '0050.TW'

data = yf.Ticker(symbol) 
ts = data.history(start='2025-01-01', end='2025-05-23')
df = pd.DataFrame(ts) 
print('len(df) = ', len(df))

# %%
from tti.indicators import MovingAverageConvergenceDivergence
adl_indicator = MovingAverageConvergenceDivergence(input_data=df)
data = adl_indicator.getTiData()
print('\MovingAverageConvergenceDivergence Technical Indicator data:\n', data)
print('len(data) = ', len(data))
# Get the most recent indicator's value
print('\nMost recent Technical Indicator value:', adl_indicator.getTiValue('2012-09-06'))
print('\nTechnical Indicator signal:', adl_indicator.getTiSignal())
adl_indicator.getTiGraph().show()

