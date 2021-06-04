"""
Module for cleaning main dataframe.
"""
import pandas

from settings import params
from settings.params import reports
from services.utils import timeit


class CleaningData:

    def __init__(self, dataframe: pandas.DataFrame):
        self.dataframe = dataframe.copy()

    @timeit
    def delete_extra_cols(self, cols: list) -> pandas.DataFrame:
        """
        Deletes extra columns from dataset.
        :param cols: list of columns for delete
        :return: dataframe without extra columns
        """
        try:
            self.dataframe = self.dataframe.drop(cols, axis=1)
            return self.dataframe
        except IndexError:
            print('error: Cols not in index of cols')

    @timeit
    def delete_rows_without_target(self) -> pandas.DataFrame:
        """
        Removes lines with no target value.
        :return: dataframe without no targeting rows
        """
        self.dataframe = self.dataframe[
            self.dataframe[params.target_cols].notnull()
        ]
        return self.dataframe

    @timeit
    def delete_empty_cols(self) -> pandas.DataFrame:
        """
        Removes columns with poorly populated data.
        :return: dataframe with reach populated cols
        """
        full_cols = []
        for col in self.dataframe.columns:
            if self.dataframe[col].isnull().sum() / len(self.dataframe) < params.BAD_FULLNESS_RATE:
                full_cols.append(col)
        self.dataframe = self.dataframe[full_cols]
        return self.dataframe

    @timeit
    def filling_missing_data(self) -> pandas.DataFrame:
        """
        Filling in missing data based on available data.
        :return: dataframe with reach populated cols
        """
        self.dataframe = self.dataframe.fillna(method='backfill')
        return self.dataframe

    @timeit
    def cols_to_datetime(self, cols: list) -> pandas.DataFrame:
        """
        Transforming objects of dataframes to datetime.
        :param cols: List of objects cols
        :return: Dataframe with datetime cols
        """
        for col in cols:
            try:
                self.dataframe[col] = pandas.to_datetime(self.dataframe[col])
            except KeyError:
                pass
        return self.dataframe

    @timeit
    def save_data(self) -> None:
        self.dataframe.to_parquet('data_clean.parquet')


if __name__ == '__main__':
    cd = CleaningData(pandas.read_parquet(reports['RawData']))
    cd.delete_extra_cols(params.extra_cols)
    cd.delete_rows_without_target()
    cd.delete_empty_cols()
    cd.filling_missing_data()
    cd.cols_to_datetime(params.datetime_cols)
    cd.save_data()
