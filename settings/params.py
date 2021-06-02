"""
Params for project setting.
"""

import os

# Data
RAW_DATA_DIRECTORY = os.path.abspath('../data')
FEATURES_DATA_DIRECTORY = os.path.abspath('../features')

# Models
RANDOM_SEED = 42
TEST_SIZE = 0.2
TIME_SLICE = 365

# Logs
LOGS_DIRECTORY = os.path.abspath('../logs')

# Reports
reports = {
    'BalanceSheet': f'{RAW_DATA_DIRECTORY}/Balance_Sheet_report.parquet',
    'CashFlow': f'{RAW_DATA_DIRECTORY}/Cash_Flow_report.parquet',
    'IncomeStatement': f'{RAW_DATA_DIRECTORY}/Income_Statement_report.parquet',
    'SP500': f'{RAW_DATA_DIRECTORY}/Index_500.parquet',
    'Stock': f'{RAW_DATA_DIRECTORY}/Stock_Quotes_Dataframe.parquet',
    'StockRelative': f'{RAW_DATA_DIRECTORY}/Stock_Quotes_Relative.parquet',
    'RawData': f'{RAW_DATA_DIRECTORY}/data.parquet',
    'FeaturesData': f'{FEATURES_DATA_DIRECTORY}/data.parquet'
}
