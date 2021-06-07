"""
Module for cleaning main dataframe.
"""
import pandas

from settings import params
from settings.params import reports


class CleaningData:

    def __init__(self, dataframe: pandas.DataFrame):
        self.dataframe = dataframe.copy()

    def delete_extra_cols(self, cols: list) -> None:
        """
        Deletes extra columns from dataset.
        :param cols: list of columns for delete
        :return: None
        """
        try:
            self.dataframe = self.dataframe.drop(cols, axis=1)
        except IndexError:
            print('error: Cols not in index of cols')

    def delete_rows_without_target(self, target) -> None:
        """
        Removes lines with no target value.
        :param target: target cols
        :return: None
        """
        self.dataframe[target] = self.dataframe[target].astype(float)
        self.dataframe = self.dataframe[
            self.dataframe[target].notnull()
        ]

    def delete_empty_cols(self) -> None:
        """
        Removes columns with poorly populated data.
        :return: None
        """
        full_cols = []
        for col in self.dataframe.columns:
            if self.dataframe[col].isnull().sum() / len(self.dataframe) \
                    < params.BAD_FULLNESS_RATE:
                full_cols.append(col)
        self.dataframe = self.dataframe[full_cols]

    def filling_missing_data(self) -> None:
        """
        Filling in missing data based on available data.
        :return: None
        """
        self.dataframe = self.dataframe.fillna(method='backfill')

    def delete_empty_rows(self) -> None:
        """
        Removes rows with Nan.
        :return: None
        """
        self.dataframe = self.dataframe.dropna(axis=0)

    def cols_to_datetime(self, cols: list) -> None:
        """
        Transforming objects of dataframes to datetime.
        :param cols: List of objects cols
        :return: None
        """
        for col in cols:
            try:
                self.dataframe[col] = pandas.to_datetime(self.dataframe[col])
            except KeyError:
                pass

    def save_data(self) -> None:
        self.dataframe.to_parquet('data_clean.parquet')


if __name__ == '__main__':
    cd = CleaningData(pandas.read_parquet(reports['RawData']))
    cd.delete_extra_cols(params.extra_cols)
    cd.delete_rows_without_target(params.target_cols[0])
    cd.delete_empty_cols()
    cd.filling_missing_data()
    cd.delete_empty_rows()
    cd.cols_to_datetime(params.datetime_cols)
    cd.save_data()
