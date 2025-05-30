# https://vectorbt.dev/
import numpy as np
import pandas as pd
from datetime import datetime

import vectorbt as vbt

# Prepare data
start = '2020-01-01 UTC'  # crypto is in UTC
end = '2025-05-23 UTC'
price = vbt.YFData.download('BTC-USD', start=start, end=end).get('Close')
print('price:',price)
fast_ma = vbt.MA.run(price, [10, 30], short_name='fast')
slow_ma = vbt.MA.run(price, [20, 60], short_name='slow')

entries = fast_ma.ma_crossed_above(slow_ma)
print('entries', entries)

exits = fast_ma.ma_crossed_below(slow_ma)
print('exits', exits)

pf = vbt.Portfolio.from_signals(price, entries, exits)
print(pf.total_return())
print(pf.stats())
