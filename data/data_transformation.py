"""
Module for transformation raw data from some sources to joined `main` dataframe.
"""
import datetime
import pandas
import pandas as pd

from settings import params
from services.utils import timeit
from settings.params import reports
from data_cleaning import CleaningData


@timeit
def _create_target(stock: pd.DataFrame, data: pd.DataFrame) -> None:
    """
    Creates dataframe: stock + joined report.
    :param stock: dataframe with stock quotes
    :param data: joined dataframe with financials indicators
    :return: None
    """

    def _computing_cumulative_product(row: pd.Series) -> float:
        """
        Return cumulative product over a rows in the main dataframe.
        :param row: row in the main dataframe
        :return: cumulative product
        """
        cumulative_product = None
        start = row['alter_filing_date']
        end = start + datetime.timedelta(params.TIME_SLICE)
        ticker = row['ticker']
        try:
            cumulative_product = stock[
                (stock['date'] >= start) &
                (stock['date'] <= end)
                ][ticker].cumprod().iloc[-1]
        except (IndexError, KeyError):
            print('error: Ticker not found')
        return cumulative_product

    cd = CleaningData(data)
    data = cd.cols_to_datetime(['date', 'filing_date',
                                'filing_date_x', 'filing_date_y'])

    data['full_filing_date'] = data.apply(_max_filing_date, axis=1)
    data['alter_filing_date'] = data.apply(_alter_filing_date, axis=1)

    data['y_1y'] = data.apply(
        lambda x: _computing_cumulative_product(x),  # Data from stock
        axis=1                                       # Computing cumprod row by row
    )
    data.to_parquet('data.parquet')


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


def _alter_filing_date(row: pd.Series) -> pd.Timestamp:
    """
    Alternative date filing if null.
    :param row: Series with timestamp
    :return: date + 40 days if null or exist filing date
    """
    instance = row['full_filing_date']
    if isinstance(instance, pd.Timestamp):
        return row['full_filing_date']
    else:
        return row['date'] + datetime.timedelta(40)


def _max_filing_date(row: pd.Series) -> pd.Timestamp:
    """
    Return not null timestamp from all filing dates in main dataframe.
    :param row: Series with timestamp in main dataframe
    :return: not null timestamp
    """
    tmp_list = [
        row['filing_date'],
        row['filing_date_x'],
        row['filing_date_y']
    ]
    for i in tmp_list:
        if isinstance(i, pd.Timestamp):
            return i


if __name__ == '__main__':
    pass
    # _percentage_change('SP500', 'Stock')
    # _joining_reports()
    # _alter_filing()
    _create_target(reports['StockRelative'], reports['RawData'])
