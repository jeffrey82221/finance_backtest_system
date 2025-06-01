import numpy as np
import pandas as pd
from datetime import datetime
from ta import add_all_ta_features
from ta import (
    add_momentum_ta,    
    add_trend_ta,
    add_volatility_ta,
    add_volume_ta,
    add_others_ta
)
from extend_input import import_custom_stock_data
import vectorbt as vbt


# Prepare data
start_date = '2025-01-01'  # crypto is in UTC
end_date = '2025-05-23'
downloaded_google_data = import_custom_stock_data('GOOG', start_date, end_date)

all_indicators = add_all_ta_features(
    downloaded_google_data.copy(),
    open='Open',
    high='High',
    low='Low',
    close='Close',
    volume='Volume',
    fillna=True
).columns
print('all_indicators:', all_indicators)

trend_indicators = add_trend_ta(
    downloaded_google_data.copy(),
    high='High',
    low='Low',
    close='Close',
    fillna=True
).columns
print('trend_indicators:', trend_indicators)

