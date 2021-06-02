"""
Module for transformation raw data from some sources to joined `main` dataframe.
"""
import pandas

from services.utils import timeit
from settings.params import reports


@timeit
def _joining_reports():
    """
    Create joined financial dataframe from several financials reports.
    """
    # Opening reports
    balance = pandas.read_parquet(reports['BalanceSheet'])
    cash = pandas.read_parquet(reports['CashFlow'])
    income = pandas.read_parquet(reports['IncomeStatement'])

    # Creates key for merging reports
    balance['key'] = balance['date'].astype(str) + balance['ticker'].astype(str)
    cash['key'] = cash['date'].astype(str) + cash['ticker'].astype(str)
    income['key'] = income['date'].astype(str) + income['ticker'].astype(str)

    # Merging reports on created key
    dataframe = income.merge(
        balance, how='inner', on='key'
    ).merge(
        cash, how='inner', on='key'
    )
    dataframe.to_parquet('data.parquet')


@timeit
def _percentage_change(index: str, stock: str) -> None:
    """
    Percentage change between the current and a prior element.
    :index: dataframe with index ticker
    :stock: dataframe with stock tickers
    :return: dataframe without market noise
    """
    dataframe = _concatenate_dataframes(index, stock)
    relative_dataframe = pandas.DataFrame()
    try:
        dataframe = dataframe.copy()
        reshaped_dataframe = dataframe.pivot(columns='ticker', values='adjclose')
        percentage_dataframe = reshaped_dataframe.pct_change()  # Percentage change
        relative_dataframe = percentage_dataframe.subtract(percentage_dataframe['^GSPC'], axis='rows') + 1.
        print(relative_dataframe)
    except KeyError:
        print('error: Ticker not found')
    relative_dataframe.to_parquet('Stock_Quotes_Relative.parquet')


def _concatenate_dataframes(name_1: str, name_2: str):
    """
    Concatenate dataframes from Yahoo Finance.
    :param name_1: Dataframe 1 name
    :param name_2: Dataframe 2 name
    :return: Concatenated dataframe
    """
    concatenated_dataframe = pandas.DataFrame()
    try:
        dataframe_1 = pandas.read_parquet(reports[name_1])
        dataframe_2 = pandas.read_parquet(reports[name_2])
        concatenated_dataframe = concatenated_dataframe.append(dataframe_1)
        concatenated_dataframe = concatenated_dataframe.append(dataframe_2)
    except FileNotFoundError:
        print('error: File not found')
    return concatenated_dataframe


@timeit
def _creating_target():
    pass


if __name__ == '__main__':
    pass
    # _percentage_change('SP500', 'Stock')
    _joining_reports()
