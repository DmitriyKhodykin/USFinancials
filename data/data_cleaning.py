"""
Module for cleaning main dataframe.
"""
import pandas

from settings.params import reports
from services.utils import timeit


class CleaningData:

    def __init__(self, dataframe: pandas.DataFrame):
        self.dataframe = dataframe.copy()

    @timeit
    def delete_extra_cols(self, cols: list) -> pandas.DataFrame:
        """
        Delete extra columns from dataset.
        :param cols: list of columns for delete
        :return: dataframe without extra columns
        """
        try:
            self.dataframe = self.dataframe.drop(cols, axis=1)
            return self.dataframe
        except IndexError:
            print('error: Cols not in index of cols')

    @timeit
    def cols_to_datetime(self, cols: list) -> pandas.DataFrame:
        """
        Transforming objects of dataframes to datetime.
        :param cols: List of objects cols
        :return: Dataframe with datetime cols
        """
        try:
            for col in cols:
                self.dataframe[col] = pandas.to_datetime(self.dataframe[col])
            return self.dataframe
        except ValueError:
            print('error: Objects are not in datetime format')
        return self.dataframe

    @timeit
    def save_data(self):
        self.dataframe.to_parquet('data_clean.parquet')


if __name__ == '__main__':
    cd = CleaningData(pandas.read_parquet(reports['RawData']))
    cd.delete_extra_cols(['currency_symbol', 'currency_symbol_x', 'currency_symbol_y', 'date_x',
                          'date_y', 'filing_date', 'filing_date_x', 'filing_date_y', 'netIncome_y',
                          'ticker_x', 'ticker_y'])
    cd.cols_to_datetime(['full_filing_date', 'alter_filing_date'])
    cd.save_data()
