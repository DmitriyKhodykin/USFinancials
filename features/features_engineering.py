"""
Features Engineering module for main dataframe.
"""
import pandas

from settings.config import reports


class FeaturesEngineering:
    """
    Engineering new features for main dataframe.
    """
    def __init__(self):
        self.dataframe = pandas.read_parquet(reports['CleanData'])

    def transformations(self):
        pass
        # Some transformations

    def save_data(self):
        self.dataframe.to_parquet('data_features.parquet')


if __name__ == '__main__':
    fe = FeaturesEngineering()
    fe.transformations()
    fe.save_data()
