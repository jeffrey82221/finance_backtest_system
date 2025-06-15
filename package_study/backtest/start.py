"""
Dollar Cost Averaging (DCA) Backtest Script
"""
import pandas as pd
import backtesting
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting._util import _Data, _Array
import math
from icecream import ic
class DCA(Strategy):

    amount_to_invest = 100

    def init(self):
        print('START init')
        print('self.data:', type(self.data))
        data: _Data = self.data
        close: _Array = data.Close
        print('self.data.Close.s:', type(self.data.Close.s))
        s: pd.core.series.Series = close.s
        print('self.I:', self.I) # get identifier of the strategy
        self.day_of_week = self.I(lambda x: x,
                                  self.data.Close.s.index.dayofweek, 
                                  plot=False)
        self.backtest_day_id = self.I(lambda x: x,
                                      range(len(self.data.Close.s.index)),
                                      plot=False)
        self.end_id = len(self.data) - 1
        print('end id:', self.end_id)
        print('END init')
        self.total_shares_bought = 0.
    def next(self):
        if self.day_of_week[-1] == 1: # Tuesday set buy order, will be tiggered on Wednesday
            num_of_shares_per_buy: int = math.floor(self.amount_to_invest / self.data.Close[-1])
            self.total_shares_bought += num_of_shares_per_buy
            ic(self.buy(
                size = num_of_shares_per_buy
                # tp = self.data.Close[-1] * 1.2,  # Take profit at 5% above the buy price
            ))
            ic(self.total_shares_bought)
            
        
print(GOOG.head())
print(GOOG.index.map(str)[-1])
GOOG = GOOG * 10 ** -6 # Scale down the data for buying micro shares
bt = Backtest(
    GOOG, 
    DCA,
    cash=10000,
    commission=0.0001, # 手續費率 
    spread=0.0005,
    hedging=False, # 是否開啟當沖交易，若無開啟（會依據先進先出法買賣股票），日內交易時才要設置
    trade_on_close=False,  # 是否在收盤時交易
    exclusive_orders=False, # 是否排除重複訂單
    finalize_trades=True,  # 是否在回測結束時自動平倉
    )
stats: backtesting._stats._Stats = bt.run()
print(stats)
trades = stats['_trades']
print(trades)
print('number of trades:', len(trades))
price_paid = trades['Size'] * trades['EntryPrice']
total_invest = price_paid.sum()
print('Total invested:', total_invest)

equity = trades['Size'] * trades['ExitPrice']
total_equity = equity.sum()
print('Total equity:', total_equity)
print('Earning:', (total_equity - total_invest)/ total_invest * 100, '%')
bt.plot(
    plot_return=True, 
    plot_pl=True, 
    plot_volume=True, 
    plot_drawdown=True, 
    superimpose=False
)