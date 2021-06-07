"""
Features Engineering module for main dataframe.
"""
import pandas

from settings.params import reports
from services.utils import timeit


class FeaturesEngineering:
    """
    Engineering new features for main dataframe.
    """
    def __init__(self, dataframe: pandas.DataFrame):
        self.dataframe = dataframe.copy()

    def transformations(self):
        pass
        # Some transformations

    def save_data(self):
        self.dataframe.to_parquet('data_features.parquet')


if __name__ == '__main__':
    fe = FeaturesEngineering(pandas.read_parquet(reports['CleanData']))
    fe.transformations()
    fe.save_data()
