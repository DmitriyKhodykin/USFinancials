"""
Utils for optimization and task evaluation.
"""
from datetime import datetime

import pandas
from sklearn.model_selection import train_test_split

from settings import params


def timeit(func):
    """
    Counts the time taken to execute the wrapped function.
    :return: func, elapsed time
    """
    logs_directory = params.LOGS_DIRECTORY

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


def hold_out(dataframe: pandas.DataFrame):
    """
    Split arrays or matrices into random train and test subsets.
    :param dataframe: Main dataframe
    :return: Train and test subsets
    """
    dataframe = dataframe.copy()
    try:
        x = dataframe.drop(params.target_cols)
        y = dataframe[params.target_cols]
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=params.TEST_SIZE,
            random_state=params.RANDOM_SEED
        )
        return x_train, x_test, y_train, y_test
    except KeyError:
        print('error: Columns with target not found')
