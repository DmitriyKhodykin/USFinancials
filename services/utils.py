"""
Utils for optimization and task evaluation.
"""
from datetime import datetime

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
