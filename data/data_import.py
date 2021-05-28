import pandas as pd
import yahoo_fin.stock_info as si

from services.utils import timeit


@timeit
def import_index_500(ticker='^GSPC') -> pd.DataFrame:
    """
    Imports data at index S&P500 from Yahoo Finance.
    :param ticker: name of ticker from Yahoo Finance
    :return: data frame with S&P500 historical data
    """
    data = None
    try:
        data = si.get_data(ticker)[['adjclose', 'ticker']]
    except KeyError:
        print('ImportS&P500Error: Ticker not found')
    return data


if __name__ == '__main__':
    print(import_index_500())
