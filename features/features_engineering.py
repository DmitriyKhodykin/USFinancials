"""
Features Engineering module.
"""
import pandas

from settings import params
from services.utils import timeit

# Globals
DATA_DIRECTORY = params.RAW_DATA_DIRECTORY


@timeit
def _features_engineering(data: pandas.DataFrame) -> None:
    """
    Engineering new features for main dataframe.
    :param data: Cleaned dataframe
    :return: None
    """
    data = data.copy()
    # Some transformations
    data.to_parquet('data.parquet')


if __name__ == '__main__':
    _features_engineering(pandas.read_parquet(f'{DATA_DIRECTORY}/data.parquet'))
