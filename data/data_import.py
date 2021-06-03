"""
Data import module from Yahoo Finance.
"""

import time
import pandas as pd
import yahoo_fin.stock_info as si

from services.utils import timeit


@timeit
def import_index_500(ticker='^GSPC') -> None:
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
def import_stock_quotes() -> None:
    """
    Get stock quotes by tickers.
    :return: None
    """
    unique_tickers_list = pd.read_parquet('unique_tickers.parquet')
    lost_tickers = []  # Not found through the Yahoo Finance service
    stock_quotes_dataframe = pd.DataFrame()

    for index, row in unique_tickers_list.iterrows():
        try:
            tmp_dataframe = si.get_data(row['ticker'])[['adjclose', 'ticker']]  # Request
            stock_quotes_dataframe = stock_quotes_dataframe.append(tmp_dataframe)
            time.sleep(2)
        except (KeyError, AssertionError):
            lost_tickers.append(row['ticker'])

    stock_quotes_dataframe.to_parquet('Stock_Quotes_Dataframe.parquet')


@timeit
def get_unique_tickers_list() -> None:
    """
    Save unique list of tickers from reports.
    :return: None
    """
    # Load data with tickers
    balance_report = pd.read_parquet('Balance_Sheet_report.parquet')
    cash_report = pd.read_parquet('Cash_Flow_report.parquet')
    income_report = pd.read_parquet('Income_Statement_report.parquet')

    balance_tickers = not_null_tickers_checker(balance_report)
    cash_tickers = not_null_tickers_checker(cash_report)
    income_tickers = not_null_tickers_checker(income_report)

    tmp_list: list = balance_tickers + cash_tickers + income_tickers
    unique_tickers = list(set(tmp_list))
    unique_tickers = pd.DataFrame(unique_tickers, columns=['ticker'])
    unique_tickers.to_parquet('unique_tickers.parquet')


@timeit
def not_null_tickers_checker(report: pd.DataFrame) -> list:
    """
    Returns a list of tickers from report, where `filing_date` - is not null
    :return: list of tickers
    """
    not_null_tickers: list = []
    unique_ticker_list = list(set(report['ticker']))

    for ticker in unique_ticker_list:
        tmp_data_frame = report[report['ticker'] == ticker]
        date_instance = tmp_data_frame['filing_date'].max()

        if isinstance(date_instance, pd.Timestamp):
            not_null_tickers.append(ticker)

    return not_null_tickers


if __name__ == '__main__':
    get_unique_tickers_list()
    import_stock_quotes()
    import_index_500()
