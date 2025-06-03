"""
NOTE: 
    - pandas ta is better than ta
"""
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
from backtesting import Backtest, Strategy
from extend_input import import_custom_stock_data
import vectorbt as vbt

def pandas_ta_bband_indicator(data: pd.DataFrame):
    """
    Calculate Bollinger Bands using pandas_ta.
    
    :param data: DataFrame containing stock data.
    :return: DataFrame with Bollinger Bands.
    """
    import pandas_ta as pta
    bband = pta.bbands(close=data.Close.s, length=20, std=2.0, talib=True)
    result = bband.to_numpy().T
    print('[pandas_ta_bband_indicator] result.shape: ', result.shape)  # Shape: (5, 97)
    return result

def ta_bband_indicator(data: pd.DataFrame):
    """
    Calculate Bollinger Bands using pandas_ta.
    
    :param data: DataFrame containing stock data.
    :return: DataFrame with Bollinger Bands.
    """
    from ta.volatility import BollingerBands
    indicator_bb = BollingerBands(close=data.Close.s, window=20, window_dev=2.0)
    # Add Bollinger Bands features to your DataFrame
    bb_bbm = indicator_bb.bollinger_mavg()   # Middle band (moving average)
    bb_bbh = indicator_bb.bollinger_hband()  # Upper band (high)
    bb_bbl = indicator_bb.bollinger_lband()  # Lower band (low)
    result = np.vstack([bb_bbm, bb_bbh, bb_bbl])
    print('[ta_bband_indicator] result.shape:', result.shape)  # Shape: (3, 97)
    return result

def custom_bband_indicator(data: pd.DataFrame, 
                          window: int = 20, 
                          std_dev: float = 2.0) -> pd.DataFrame:
    """
    Calculate Bollinger Bands using pandas.
    
    :param data: DataFrame containing stock data.
    :param window: Window size for the moving average.
    :param std_dev: Standard deviation multiplier.
    :return: DataFrame with Bollinger Bands.
    """
    rolling_mean = data.Close.s.rolling(window=window).mean()
    rolling_std = data.Close.s.rolling(window=window).std()
    
    bb_upper = rolling_mean + (rolling_std * std_dev)
    bb_lower = rolling_mean - (rolling_std * std_dev)
    bb_upper = bb_upper.to_numpy()
    bb_lower = bb_lower.to_numpy()  
    result = np.vstack([bb_upper, bb_lower])
    print('[custom_bband_indicator] result.shape:', result.shape)  # Shape: (2, 97)
    return result
class RunInputAppendIndicator(Strategy):
    """
    Strategy to demonstrate how to append indicators to the backtesting framework.
    This strategy is used to demonstrate how to add indicators to the backtesting framework.
    It does not perform any trading actions.
    """
    def init(self):
        self.pandas_ta_bbands = self.I(
            pandas_ta_bband_indicator, 
            self.data, 
            overlay=True
        )
        self.ta_bbands = self.I(
            ta_bband_indicator, 
            self.data, 
            overlay=True
        )
        self.custom_bbands = self.I(
            custom_bband_indicator, 
            self.data, 
            overlay=True
        )
        print('[init] pandas_ta_bbands shape:', self.pandas_ta_bbands.shape)
        print('[init] ta_bbands shape:', self.ta_bbands.shape)
        print('[init] custom_bbands shape:', self.custom_bbands.shape)
        

    def next(self):
        print('[next] Appended Trend MACD:', self.data.trend_macd[-1])
        print('[next] Pandas TA BBands no.1:', self.pandas_ta_bbands[0][-1])
        print('[next] Pandas TA BBands no.2:', self.pandas_ta_bbands[1][-1])
        print('[next] Pandas TA BBands no.3:', self.pandas_ta_bbands[2][-1])
        print('[next] Pandas TA BBands no.4:', self.pandas_ta_bbands[3][-1])
        print('[next] Pandas TA BBands no.5:', self.pandas_ta_bbands[4][-1])
        print('[next] TA BBands no.1:', self.ta_bbands[0][-1])
        print('[next] TA BBands no.2:', self.ta_bbands[1][-1])
        print('[next] TA BBands no.3:', self.ta_bbands[2][-1])
        print('[next] Custom BBands no.1:', self.custom_bbands[0][-1])
        print('[next] Custom BBands no.2:', self.custom_bbands[1][-1])
        
if __name__ == '__main__':
    start_date = '2025-01-01'  # crypto is in UTC
    end_date = '2025-05-23'
    downloaded_google_data = import_custom_stock_data(
        'GOOG', start_date, end_date)
    google_with_all_indicators = add_all_ta_features(
        downloaded_google_data.copy(),
        open='Open',
        high='High',
        low='Low',
        close='Close',
        volume='Volume',
        fillna=True
    )
    print('all_indicators:', google_with_all_indicators)
    """
    trend_indicators = add_trend_ta(
        downloaded_google_data.copy(),
        high='High',
        low='Low',
        close='Close',
        fillna=True
    ).columns
    print('trend_indicators:', trend_indicators)
    """
    bt = Backtest(
        google_with_all_indicators, 
        RunInputAppendIndicator, 
        trade_on_close=False
    )
    bt.run()
    bt.plot()
