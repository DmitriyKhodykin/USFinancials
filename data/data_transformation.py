import pandas as pd

from services.utils import timeit
from settings import params


# Globals
DATA_DIRECTORY = params.RAW_DATA_DIRECTORY


@timeit
def _opening_reports(*args) -> pd.DataFrame:
    """
    Opens the required reports from the local storage.
    :param args: Names of reports
    :return: Pandas data frames
    """
    report = pd.DataFrame()
    for report_name in args:
        try:
            report = pd.read_parquet(f'{DATA_DIRECTORY}/{report_name}.parquet')
            print(f'Report {report_name} opened, count: {len(report)}')
            return report
        except KeyError:
            print(f'error: File {report_name} not found')
    return report


@timeit
def _concatenate_dataframes(name_1: str, name_2: str):
    """
    Concatenate dataframes from Yahoo Finance.
    :param name_1: Dataframe 1 name
    :param name_2: Dataframe 2 name
    :return: Concatenated dataframe
    """
    concatenated_dataframe = pd.DataFrame()
    try:
        dataframe_1 = pd.read_parquet(f'{DATA_DIRECTORY}/{name_1}.parquet')
        dataframe_2 = pd.read_parquet(f'{DATA_DIRECTORY}/{name_2}.parquet')
        concatenated_dataframe = concatenated_dataframe.append(dataframe_1)
        concatenated_dataframe = concatenated_dataframe.append(dataframe_2)
    except FileNotFoundError:
        print('error: File not found')
    return concatenated_dataframe


@timeit
def _percentage_change(index: str, stock: str) -> None:
    """
    Percentage change between the current and a prior element.
    :index: dataframe with index ticker
    :stock: dataframe with stock tickers
    :return: dataframe without market noise
    """
    dataframe = _concatenate_dataframes(index, stock)
    relative_dataframe = pd.DataFrame()
    try:
        dataframe = dataframe.copy()
        reshaped_dataframe = dataframe.pivot(columns='ticker', values='adjclose')
        percentage_dataframe = reshaped_dataframe.pct_change()  # Percentage change
        relative_dataframe = percentage_dataframe.subtract(percentage_dataframe['^GSPC'], axis='rows') + 1.
        print(relative_dataframe)
    except KeyError:
        print('error: Ticker not found')
    relative_dataframe.to_parquet('Stock_Quotes_Relative.parquet')


@timeit
def _creating_target():
    pass


@timeit
def _joining_reports() -> pd.DataFrame:

    balance, cash, income, index_sp, stock = _opening_reports('Balance_Sheet_report', 'Cash_Flow_report',
                                                              'Income_Statement_report', 'Index_500',
                                                              'Stock_Quotes_Dataframe')
    relative_stock = _percentage_change()

    data = pd.DataFrame()
    return data


if __name__ == '__main__':
    _percentage_change('Index_500', 'Stock_Quotes_Dataframe')
