"""
Dollar Cost Averaging (DCA) Backtest Script
"""
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.test import GOOG

class DCA(Strategy):
    amount_to_invest = 100

    def init(self):
        self.day_of_week = self.I(lambda x: x,
                                  self.data.Close.s.index.dayofweek)

    def next(self):
        pass

print(GOOG.head())
bt = Backtest(GOOG, DCA)

