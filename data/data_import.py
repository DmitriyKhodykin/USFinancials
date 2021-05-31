"""
Data import module from Yahoo Finance.
"""

import time
import pandas as pd
import yahoo_fin.stock_info as si

from services.utils import timeit


@timeit
def _get_unique_tickers_list() -> list:
    """
    Returns a unique list of tickers from reports.
    :return: unique list of tickers
    """
    # Load data with tickers
    balance_report = pd.read_parquet('Balance_Sheet_report.parquet')
    cash_report = pd.read_parquet('Cash_Flow_report.parquet')
    income_report = pd.read_parquet('Income_Statement_report.parquet')

    balance_tickers = balance_report['ticker'].to_list()
    cash_tickers = cash_report['ticker'].to_list()
    income_tickers = income_report['ticker'].to_list()

    tmp_list: list = balance_tickers + cash_tickers + income_tickers

    unique_tickers: list = []
    for i in tmp_list:
        if i not in unique_tickers:
            unique_tickers.append(i)

    return unique_tickers


@timeit
def _import_index_500(ticker='^GSPC') -> None:
    """
    Imports data at index S&P500 from Yahoo Finance.
    :param ticker: name of ticker from Yahoo Finance
    :return: data frame with S&P500 historical data
    """
    data = None
    try:
        data = si.get_data(ticker)[['adjclose', 'ticker']]
    except KeyError:
        print('ImportS&P500Error: Ticker not found')
    data.to_parquet('Index_500.parquet')


@timeit
def _get_stock_quotes() -> None:
    """
    Get stock quotes by tickers.
    :return: None
    """
    unique_tickers_list = _get_unique_tickers_list()
    lost_tickers = []  # Not found through the Yahoo Finance service
    stock_quotes_dataframe = pd.DataFrame()

    for ticker in unique_tickers_list:
        try:
            tmp_dataframe = si.get_data(ticker)[['adjclose', 'ticker']]  # Request
            stock_quotes_dataframe = stock_quotes_dataframe.append(tmp_dataframe)
            time.sleep(2)
        except (KeyError, AssertionError):
            lost_tickers.append(ticker)

    stock_quotes_dataframe.to_parquet('Stock_Quotes_Dataframe.parquet')


if __name__ == '__main__':
    _get_stock_quotes()
