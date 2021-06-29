"""
Predictive module through trained model.
How to get live fundamental data from Yahoo Finance:
http://theautomatic.net/2020/05/05/how-to-download-fundamentals-data-with-python/
"""

import numpy
import pickle
from yahoo_fin import stock_info

from models.models_features import best_cols_list


def predict_stock_class(ticker: str) -> int:
    """
    Predicts the success of a stock one year after filing.
    :param ticker: yahoo_fin stock name
    :return: predicted class (1 - to buy, 0 - do not to buy)
    """
    # Get data from YF
    live_data = get_live_data(ticker)

    # Load serialized model
    try:
        with open('model.pickle', 'rb') as file:
            model = pickle.load(file)
    except pickle.UnpicklingError:
        print('error: Pickle unpacking error')

    # Predict
    predicted_class = model.predict([live_data])
    print(f'Stock: {ticker}, Forecast: {predicted_class}')
    return predicted_class


def get_live_data(ticker: str, yearly=False) -> numpy.ndarray:
    """
    Obtaining the values of financial indicators required for forecasting.
    :param ticker: yahoo_fin stock name
    :param yearly: indicators in annual or quarterly terms
    :return: an array with values of important features for the forecast
    """
    # Live data from Yahoo Finance
    balance = stock_info.get_balance_sheet(ticker, yearly=yearly)
    income = stock_info.get_income_statement(ticker, yearly=yearly)
    cash = stock_info.get_cash_flow(ticker, yearly=yearly)

    # Merging dataframes
    df = balance.append(income)
    df = df.append(cash)

    # Filtering by best features (col names)
    df = df.loc[best_cols_list]  # No 'intangibleAssets', 'commonStockSharesOutstanding'
    vec = list(df.iloc[:, 0].values)

    print('Array for class predict:', vec)
    return vec


if __name__ == '__main__':
    predict_stock_class("aapl")
