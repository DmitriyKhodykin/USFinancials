"""
Utils for optimization and task evaluation.
"""
from datetime import datetime

import pandas
from sklearn.model_selection import train_test_split

from settings import config


def timeit(func):
    """
    Counts the time taken to execute the wrapped function.
    :return: func, elapsed time
    """
    logs_directory = config.LOGS_DIRECTORY

    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        elapsed_time = datetime.now() - start
        str_elapsed_time = f'func {func.__name__} args: {locals()["args"]}, ' \
                           f'elapsed time: {elapsed_time} \n'
        print(str_elapsed_time)
        with open(f'{logs_directory}/logs.txt', 'a') as log:
            log.write(str_elapsed_time)
        return result
    return wrapper


def create_binary_target(dataframe: pandas.DataFrame, target: str,
                         cut_off_value: float) -> pandas.Series:
    """
    Creates binary target from cut-off threshold value and real target
    :param dataframe: Main dataframe
    :param cut_off_value: Everything above the cut-off threshold is 1
    :param target: Name of target column
    :return: Binary target series
    """
    y_subset = dataframe[target].apply(
        lambda t: 1 if t > cut_off_value else 0
    )
    return y_subset


def split_data(dataframe: pandas.DataFrame):
    """
    Split dataframe to x subset and y subset.
    :param dataframe: Main dataframe
    :return: x, y
    """
    try:
        x = dataframe.drop(config.target_cols, axis=1)
        y = create_binary_target(
            dataframe,
            config.target_cols[0],
            config.CUT_OFF_VALUE
        )
        return x, y
    except KeyError:
        print('error: Columns with target not found')


def hold_out(dataframe: pandas.DataFrame):
    """
    Split arrays or matrices into random train and test subsets.
    :param dataframe: Main dataframe
    :return: Train and test subsets
    """
    dataframe = dataframe.copy()
    x, y = split_data(dataframe)
    try:
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=config.TEST_SIZE,
            random_state=config.RANDOM_SEED
        )
        return x_train, x_test, y_train, y_test
    except KeyError:
        print('error: Columns with target not found')
