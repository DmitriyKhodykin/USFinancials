"""
Features Engineering module.
"""
import pandas

from settings import params
from services.utils import timeit

# Globals
DATA_DIRECTORY = params.RAW_DATA_DIRECTORY


class FeaturesEngineering:
    """
    Engineering new features for main dataframe.
    :param data: Cleaned dataframe
    :return: None
    """
    def __init__(self, data: pandas.DataFrame):
        self.data = data

    @timeit
    def transformations(self):
        pass
        # Some transformations

    @timeit
    def save_data(self):
        self.data.to_parquet('data.parquet')


if __name__ == '__main__':
    fe = FeaturesEngineering(pandas.read_parquet(f'{DATA_DIRECTORY}/data.parquet'))
    fe.transformations()
    fe.save_data()
