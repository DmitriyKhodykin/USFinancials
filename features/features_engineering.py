"""
Features Engineering module for main dataframe.
"""
import pandas

from settings import config
from settings.config import reports


def main():
    fe = FeaturesEngineering()
    fe.transformations()
    fe.save_data()


class FeaturesEngineering:
    """
    Engineering new features for main dataframe.
    """
    def __init__(self):
        print(f'Loading data from {reports["CleanData"]}...')
        self.dataframe = pandas.read_parquet(reports['CleanData'])

    def transformations(self):
        print('Make some transformations...')

    def save_data(self):
        address = f'{config.FEATURES_DATA_DIRECTORY}/data_features.parquet'
        print(f'Saving to {address}...')
        self.dataframe.to_parquet(address)


if __name__ == '__main__':
    main()
