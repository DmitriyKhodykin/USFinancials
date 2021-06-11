"""
Module for cleaning main dataframe.
"""
import pandas
import pandas as pd

from settings import config
from settings.config import reports


class CleaningData:

    def __init__(self, dataframe: pandas.DataFrame):
        self.dataframe = dataframe.copy()

    def delete_extra_cols(self, cols: list) -> pd.DataFrame:
        """
        Deletes extra columns from dataset.
        :param cols: list of columns for delete
        :return: Dataframe without extra cols
        """
        try:
            self.dataframe = self.dataframe.drop(cols, axis=1)
            return self.dataframe
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

    def delete_empty_cols(self) -> pd.DataFrame:
        """
        Removes columns with poorly populated data.
        :return: Dataframe with reach populated cols
        """
        full_cols = []
        for col in self.dataframe.columns:
            if self.dataframe[col].isnull().sum() / len(self.dataframe) \
                    < config.BAD_FULLNESS_RATE:
                full_cols.append(col)
        self.dataframe = self.dataframe[full_cols]
        return self.dataframe

    def filling_missing_data(self) -> pd.DataFrame:
        """
        Filling in missing data based on available data.
        :return: Dataframe with reach populated rows
        """
        self.dataframe = self.dataframe.fillna(method='backfill')
        return self.dataframe

    def delete_empty_rows(self) -> pd.DataFrame:
        """
        Removes rows with Nan.
        :return: Dataframe with reach populated rows
        """
        self.dataframe = self.dataframe.dropna(axis=0)
        return self.dataframe

    def cols_to_datetime(self, cols: list) -> pd.DataFrame:
        """
        Transforming objects of dataframes to datetime.
        :param cols: List of objects cols
        :return: None
        """
        for col in cols:
            try:
                self.dataframe[col] = pandas.to_datetime(self.dataframe[col])
                return self.dataframe
            except KeyError:
                pass

    def delete_type_object_cols(self) -> None:
        """
        Deletes all non-float columns.
        :return: None
        """
        for i in self.dataframe.columns:
            try:
                self.dataframe[i] = self.dataframe[i].astype(float)
            except (ValueError, TypeError):
                self.dataframe.drop(i, axis=1, inplace=True)

    def save_data(self) -> None:
        self.dataframe.to_parquet('data_clean.parquet')


if __name__ == '__main__':
    cd = CleaningData(pandas.read_parquet(reports['RawData']))
    cd.delete_extra_cols(config.extra_cols)
    cd.delete_rows_without_target(config.target_cols[0])
    cd.delete_empty_cols()
    cd.filling_missing_data()
    cd.delete_empty_rows()
    cd.delete_type_object_cols()
    cd.save_data()
