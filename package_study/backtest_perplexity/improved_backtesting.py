
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG  # 雿輻鍂�批遣皜祈岫鞈��
import pandas_ta as ta
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


class ImprovedMacdRsiKdjStrategy(Strategy):
    # 策略參數
    rsi_length = 14
    kdj_length, kdj_signal = 9, 3
    ma_length = 200  # 移動平均線長度
    risk_per_trade = 0.02  # 單筆交易風險 2%
    atr_length = 14  # ATR 參數
    atr_multiplier = 2.0  # ATR 倍數

    def init(self):
        # 初始化指標
        self.macd_hist = self.I(
            partial(adapt_ta(ta.macd), fast=12, slow=26, signal=9, output_idx=1), 
            self.data, 
            overlay=True
        )
        self.macd_line = self.I(
            partial(adapt_ta(ta.macd), fast=12, slow=26, signal=9, output_idx=0), 
            self.data, 
            overlay=True
        )
        self.macd_signal = self.I(
            partial(adapt_ta(ta.macd), fast=12, slow=26, signal=9, output_idx=2), 
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

        # 200 日移動平均線
        self.ma200 = self.I(
            partial(adapt_ta(ta.sma), length=self.ma_length), 
            self.data, 
            overlay=True
        )

        # ATR 指標
        self.atr = self.I(
            partial(adapt_ta(ta.atr), length=self.atr_length), 
            self.data, 
            overlay=True
        )

        # 紀錄進場價格與止損價格
        self.entry_price = None
        self.stop_loss = None

    def calculate_position_size(self, stop_distance):
        """計算交易倉位大小"""
        if stop_distance <= 0:
            return 0

        risk_amount = self.equity * self.risk_per_trade
        shares = int(risk_amount / stop_distance)
        max_shares = int(self.equity * 0.95 / self.data.Close[-1])  # 最大倉位限制為 95%

        return min(shares, max_shares)

    def get_signal_strength(self):
        """計算多空信號強度 (0-3 級)"""
        score = 0

        # MACD 信號
        macd_bullish = (self.macd_hist[-1] > 0 and self.macd_hist[-1] > self.macd_hist[-2]) or                       (crossover(self.macd_line, self.macd_signal))
        macd_bearish = (self.macd_hist[-1] < 0 and self.macd_hist[-1] < self.macd_hist[-2]) or                       (crossover(self.macd_signal, self.macd_line))

        # RSI 信號  
        rsi_bullish = (self.rsi[-1] < 50 and self.data.Close[-1] > self.data.Close[-2])
        rsi_bearish = (self.rsi[-1] > 50 and self.data.Close[-1] < self.data.Close[-2])

        # KDJ 信號
        kdj_bullish = crossover(self.k, self.d) and self.j[-1] < 80
        kdj_bearish = crossover(self.d, self.k) and self.j[-1] > 20

        # 計算多空信號總數
        bullish_signals = sum([macd_bullish, rsi_bullish, kdj_bullish])
        bearish_signals = sum([macd_bearish, rsi_bearish, kdj_bearish])

        return bullish_signals, bearish_signals

    def next(self):
        if len(self.data.Close) < max(self.ma_length, 20):
            return

        # 趨勢判斷
        is_uptrend = self.data.Close[-1] > self.ma200[-1]
        is_downtrend = self.data.Close[-1] < self.ma200[-1]

        bullish_signals, bearish_signals = self.get_signal_strength()

        # 強多空信號
        strong_bullish = bullish_signals >= 2 and is_uptrend
        strong_bearish = bearish_signals >= 2 and is_downtrend

        # ATR 止損距離
        atr_stop_distance = self.atr[-1] * self.atr_multiplier

        # 開倉
        if not self.position:
            if strong_bullish:
                # 多頭開倉
                position_size = self.calculate_position_size(atr_stop_distance)
                if position_size > 0:
                    self.buy(size=position_size)
                    self.entry_price = self.data.Close[-1]
                    self.stop_loss = self.entry_price - atr_stop_distance

            elif strong_bearish:
                # 空頭開倉
                position_size = self.calculate_position_size(atr_stop_distance)
                if position_size > 0:
                    self.sell(size=position_size)
                    self.entry_price = self.data.Close[-1]
                    self.stop_loss = self.entry_price + atr_stop_distance

        # 平倉
        else:
            if self.position.is_long:
                # 多頭平倉條件
                stop_hit = self.data.Close[-1] <= self.stop_loss
                rsi_overbought = self.rsi[-1] > 70
                bearish_reversal = bearish_signals >= 2
                trend_broken = self.data.Close[-1] < self.ma200[-1]

                if stop_hit or rsi_overbought or bearish_reversal or trend_broken:
                    self.position.close()
                    self.entry_price = None
                    self.stop_loss = None

            elif self.position.is_short:
                # 空頭平倉條件  
                stop_hit = self.data.Close[-1] >= self.stop_loss
                rsi_oversold = self.rsi[-1] < 30
                bullish_reversal = bullish_signals >= 2
                trend_broken = self.data.Close[-1] > self.ma200[-1]

                if stop_hit or rsi_oversold or bullish_reversal or trend_broken:
                    self.position.close()
                    self.entry_price = None
                    self.stop_loss = None


class OriginalMacdRsiKdjStrategy(Strategy):
    """原始的MACD、RSI、KDJ策略"""
    rsi_length = 14
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
        if len(self.data.Close) < 3:
            return

        # �笔�憭𡁻�璇苷辣
        bullish_macd = (self.macd_hist[-1] > 0) and (self.macd_hist[-1] > self.macd_hist[-2])
        bullish_rsi = (self.rsi[-1] < 50) and (self.data.Close[-3] < self.data.Close[-2] < self.data.Close[-1])
        bullish_kdj = crossover(self.k, self.d) and (self.j[-1] < 80)

        # �笔�蝛粹�璇苷辣
        bearish_macd = (self.macd_hist[-1] < 0) and (self.macd_hist[-1] > self.macd_hist[-2])
        bearish_rsi = (self.rsi[-1] > 50) and (self.data.Close[-3] > self.data.Close[-2] > self.data.Close[-1])
        bearish_kdj = crossover(self.d, self.k) and (self.j[-1] > 20)

        # 鈭斗��讛摩
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


def run_comparison():
    """比較策略表現"""
    print("=== 比較策略表現 ===\n")

    # 原始策略
    bt_original = Backtest(
        GOOG,
        OriginalMacdRsiKdjStrategy,
        cash=10000,
        commission=0.002,
        exclusive_orders=True
    )

    result_original = bt_original.run()

    # 改進策略
    bt_improved = Backtest(
        GOOG,
        ImprovedMacdRsiKdjStrategy,
        cash=10000,
        commission=0.002,
        exclusive_orders=True
    )

    result_improved = bt_improved.run()

    print("原始策略結果:")
    print(f"總回報: {result_original['Return [%]']:.2f}%")
    print(f"年化回報: {result_original['Return (Ann.) [%]']:.2f}%")
    print(f"夏普比率: {result_original['Sharpe Ratio']:.3f}")
    print(f"最大回撤: {result_original['Max. Drawdown [%]']:.2f}%")
    print(f"交易次數: {result_original['# Trades']}")
    print(f"勝率: {result_original['Win Rate [%]']:.2f}%")
    print(f"資金暴露時間: {result_original['Exposure Time [%]']:.2f}%\n")

    print("改進策略結果:")
    print(f"總回報: {result_improved['Return [%]']:.2f}%")
    print(f"年化回報: {result_improved['Return (Ann.) [%]']:.2f}%")
    print(f"夏普比率: {result_improved['Sharpe Ratio']:.3f}")
    print(f"最大回撤: {result_improved['Max. Drawdown [%]']:.2f}%")
    print(f"交易次數: {result_improved['# Trades']}")
    print(f"勝率: {result_improved['Win Rate [%]']:.2f}%")
    print(f"資金暴露時間: {result_improved['Exposure Time [%]']:.2f}%\n")

    # 比較改進幅度
    return_improvement = result_improved['Return [%]'] - result_original['Return [%]']
    trades_improvement = result_improved['# Trades'] - result_original['# Trades']

    print("=== 改進幅度 ===")
    print(f"總回報改進: {return_improvement:.2f}%")
    print(f"交易次數增減: {trades_improvement}")
    print(f"夏普比率改進: {result_improved['Sharpe Ratio'] - result_original['Sharpe Ratio']:.3f}")

    return result_original, result_improved


if __name__ == '__main__':
    # 執行策略比較
    original_result, improved_result = run_comparison()