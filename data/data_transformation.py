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
def create_target(stock: str, data: str) -> None:
    """
    Creates dataframe: stock + joined report.
    :param stock: dataframe with stock quotes
    :param data: joined dataframe with financials indicators
    :return: None
    """
    # Open dataframes
    dataframe_stock = pd.read_parquet(reports[stock])
    dataframe_data = pd.read_parquet(reports[data])

    def computing_cumulative_product(row: pd.Series) -> float:
        """
        Return cumulative product over a rows in the main dataframe.
        :param row: row in the main dataframe
        :return: cumulative product
        """
        start = row['alter_filing_date']
        end = start + datetime.timedelta(params.TIME_SLICE)
        ticker = row['ticker']
        try:
            cumulative_product = dataframe_stock[
                (dataframe_stock['date'] >= start) &
                (dataframe_stock['date'] <= end)
                ][ticker].cumprod().iloc[-1]
            return cumulative_product
        except (IndexError, KeyError):
            print('error: Ticker not found')

    cd = CleaningData(dataframe_data)  # Change object type to datetime
    dataframe_data = cd.cols_to_datetime(params.datetime_cols)
    dataframe_stock['date'] = dataframe_stock.index

    # Return best series with [filing date] from financials reports
    dataframe_data['full_filing_date'] = dataframe_data.apply(max_filing_date, axis=1)

    # If [filing date] is null, [date] + 40 days
    dataframe_data['alter_filing_date'] = dataframe_data.apply(alter_filing_date, axis=1)

    # Create target as cumprod on TIME_SLICE
    dataframe_data['y_1y'] = dataframe_data.apply(computing_cumulative_product, axis=1)

    # Save main dataframe
    dataframe_data.to_parquet('data.parquet')


@timeit
def joining_reports():
    """
    Creates joined financial dataframe from several financials reports.
    """
    # Open reports
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
def percentage_change(index: str, stock: str) -> None:
    """
    Percentage change between the current and a prior element.
    :index: dataframe with index ticker
    :stock: dataframe with stock tickers
    :return: dataframe without market noise
    """
    dataframe = concatenate_dataframes(index, stock)
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


def concatenate_dataframes(name_1: str, name_2: str):
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


def alter_filing_date(row: pd.Series) -> pd.Timestamp:
    """
    Alternative date filing if null.
    :param row: Series with timestamp
    :return: <date + ALTER FILING DAYS> if null, or exist filing date
    """
    instance = row['full_filing_date']
    if isinstance(instance, pd.Timestamp):
        return row['full_filing_date']
    else:
        return row['date'] + datetime.timedelta(params.ALTER_FILING_DAYS)


def max_filing_date(row: pd.Series) -> pd.Timestamp:
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
    percentage_change('SP500', 'Stock')
    joining_reports()
    create_target('StockRelative', 'RawData')
