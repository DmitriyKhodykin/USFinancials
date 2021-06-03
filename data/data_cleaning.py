"""
Module for cleaning main dataframe.
"""
import pandas


class CleaningData:

    def __init__(self, dataframe: pandas.DataFrame):
        self.dataframe = dataframe.copy()

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


if __name__ == '__main__':
    pass
