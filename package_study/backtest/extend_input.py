"""
Dollar Cost Averaging (DCA) Backtest Script
"""
import pandas as pd
import backtesting
from backtesting import Backtest
from backtesting.test import GOOG
import yfinance as yf

def import_default_stock_data():
    """
    Import default stock data for backtesting.
    """
    return GOOG

def import_custom_stock_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Import custom stock data from Yahoo Finance.
    
    :param symbol: Stock symbol to import.
    :param start: Start date for the data.
    :param end: End date for the data.
    :return: DataFrame containing stock data.
    """
    data = yf.Ticker(symbol)
    ts = data.history(start=start, end=end)
    return pd.DataFrame(ts)[['Open', 'High', 'Low', 'Close', 'Volume']]

def assert_data_type_consistency(default_stock_data: pd.DataFrame, custom_stock_data: pd.DataFrame):
    """
    Assert that the DataFrame contains consistent data types.
    
    :param df: DataFrame to check.
    """
    assert isinstance(default_stock_data, pd.DataFrame), "Default stock data is not a DataFrame"
    assert isinstance(custom_stock_data, pd.DataFrame), "Custom stock data is not a DataFrame"
    assert default_stock_data.shape[0] > 0, "Default stock data is empty"
    assert custom_stock_data.shape[0] > 0, "Custom stock data is empty"
    assert default_stock_data.shape[1] == custom_stock_data.shape[1], "DataFrames have different number of columns"
    assert set(default_stock_data.columns) == set(custom_stock_data.columns), "DataFrames have different columns"
    assert default_stock_data.dtypes.equals(custom_stock_data.dtypes), "DataFrames have different data types"

def plot_and_compare_stock_data(default_stock_data: pd.DataFrame, custom_stock_data: pd.DataFrame):
    """
    Plot stock data for comparison.
    
    :param default_stock_data: Default stock data DataFrame.
    :param custom_stock_data: Custom stock data DataFrame.
    """
    default_stock_data_first = default_stock_data['Open'].iloc[0]
    custom_stock_data_first = custom_stock_data['Open'].iloc[0]

    for col in ['Open', 'High', 'Low', 'Close']:
        default_stock_data[col] = default_stock_data[col] / default_stock_data_first
        custom_stock_data[col] = custom_stock_data[col] / custom_stock_data_first
        
    print('Default stock data:', default_stock_data)
    print('Custom stock data:', custom_stock_data)

    # Plot the open price of the default against that of the custom stock data
    default_stock_data['Open'].plot(label='Default Google Open Price')
    custom_stock_data['Open'].plot(label='Custom Google Open Price')
    import matplotlib.pyplot as plt
    plt.legend()
    plt.title('Open Price Comparison')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

if __name__ == "__main__":
    google_data = import_default_stock_data()
    # get start date of the google data
    start_date = google_data.index.min().strftime('%Y-%m-%d')
    # get end date + one day of the google data
    end_date = (google_data.index.max() + pd.Timedelta(days=1)).strftime('%Y-%m-%d')

    downloaded_google_data = import_custom_stock_data('GOOG', start_date, end_date)


    print('Default stock data:', google_data)
    print('Custom stock data:', downloaded_google_data)

    assert_data_type_consistency(
        google_data, downloaded_google_data
    )

    # NOTE: Check by normalizing the data

    # Normalized the google_data to the same scale as the downloaded data
    # Only normalized the price related columns use for loops to avoid hardcoding column names
    plot_and_compare_stock_data(
        google_data.copy(), downloaded_google_data.copy()
    )