from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG  # 使用內建測試資料
import pandas_ta as ta
import pandas as pd
from icecream import ic
from functools import partial


def adapt_ta(pandas_ta_func):
    """
    Decorator to add an indicator to the strategy.
    
    :param func: Function to be decorated.
    :return: Decorated function.
    """
    def wrapper(data, **kwargs):
        signals = pandas_ta_func(
            high=data.High.s, 
            low=data.Low.s, 
            close=data.Close.s,
            volume=data.Volume.s,
            open=data.Open.s,
            **kwargs)
        result = signals.to_numpy().T
        if len(result.shape) > 1:
            result = result[kwargs['output_idx']] 
        return result
    return wrapper


class MacdRsiKdjStrategy(Strategy):
    # RSI 參數
    rsi_length = 14
    # KDJ 參數
    kdj_length, kdj_signal = 9, 3

    def init(self):
        self.macd_hist = self.I(
            partial(adapt_ta(ta.macd), fast=12, slow=26, signal=9, output_idx=1), 
            self.data, 
            overlay=True
        )
        self.rsi = self.I(
            partial(adapt_ta(ta.rsi), length=14), 
            self.data, 
            overlay=True
        )
        self.k = self.I(
            partial(adapt_ta(ta.kdj), length=9, signal=3, output_idx=0), 
            self.data, 
            overlay=True
        )
        self.d = self.I(
            partial(adapt_ta(ta.kdj), length=9, signal=3, output_idx=1), 
            self.data, 
            overlay=True
        )
        self.j = self.I(
            partial(adapt_ta(ta.kdj), length=9, signal=3, output_idx=2), 
            self.data, 
            overlay=True
        )

    def next(self):
        if len(self.data.Close) < 3:  # 確保有足夠的歷史數據
            return
        
        # 多頭條件
        bullish_macd = (self.macd_hist[-1] > 0) and (self.macd_hist[-1] > self.macd_hist[-2])
        bullish_rsi = (self.rsi[-1] < 50) and (self.data.Close[-3] < self.data.Close[-2] < self.data.Close[-1])
        bullish_kdj = crossover(self.k, self.d) and (self.j[-1] < 80)
        
        # 空頭條件
        bearish_macd = (self.macd_hist[-1] < 0) and (self.macd_hist[-1] > self.macd_hist[-2])
        bearish_rsi = (self.rsi[-1] > 50) and (self.data.Close[-3] > self.data.Close[-2] > self.data.Close[-1])
        bearish_kdj = crossover(self.d, self.k) and (self.j[-1] > 20)

        # 交易邏輯
        if not self.position:
            if bullish_macd and bullish_rsi and bullish_kdj:
                self.buy()
            elif bearish_macd and bearish_rsi and bearish_kdj:
                self.sell()
        else:
            if self.position.is_long and (bearish_kdj or self.rsi[-1] > 70):
                self.position.close()
            elif self.position.is_short and (bullish_kdj or self.rsi[-1] < 30):
                self.position.close()

if __name__ == '__main__':
    bt = Backtest(
        GOOG,
        MacdRsiKdjStrategy,
        cash=10000,
        commission=0.002,
        exclusive_orders=True
    )

    output = bt.run()
    bt.plot()
    print(output)
    # This code is not winning