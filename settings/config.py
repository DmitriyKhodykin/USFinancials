"""
Configuration for project setting.
"""

import os

# Data
DATA_DIRECTORY = 'data'
RAW_DATA_DIRECTORY = os.path.abspath('../data')
FEATURES_DATA_DIRECTORY = os.path.abspath('../features')

# Logs
LOGS_DIRECTORY = os.path.abspath('../logs')

# Globals for data pipeline
TIME_SLICE = 365         # Days from filing date
ALTER_FILING_DAYS = 40   # + date, if filing date is null
BAD_FULLNESS_RATE = 0.3  # % empty values in col for delete col
CUT_OFF_VALUE = 1.05     # For binary target

# Models
RANDOM_SEED = 42
TEST_SIZE = 0.2

# Reports
reports = {
    'BalanceSheet': f'{RAW_DATA_DIRECTORY}/Balance_Sheet_report.parquet',
    'CashFlow': f'{RAW_DATA_DIRECTORY}/Cash_Flow_report.parquet',
    'IncomeStatement': f'{RAW_DATA_DIRECTORY}/Income_Statement_report.parquet',
    'SP500': f'{RAW_DATA_DIRECTORY}/Index_500.parquet',
    'Stock': f'{RAW_DATA_DIRECTORY}/Stock_Quotes_Dataframe.parquet',
    'StockRelative': f'{RAW_DATA_DIRECTORY}/Stock_Quotes_Relative.parquet',
    'RawData': f'{RAW_DATA_DIRECTORY}/data.parquet',
    'CleanData': f'{RAW_DATA_DIRECTORY}/data_clean.parquet',
    'FeaturesData': f'{FEATURES_DATA_DIRECTORY}/data_features.parquet'
}

# COLUMNS IN MAIN DATAFRAME

# Extra columns in main dataframe (delete by data_cleaning module)
extra_cols = [
    'commonStockSharesOutstanding',
    'currency_symbol',
    'currency_symbol_x',
    'currency_symbol_y',
    'date_x',
    'date_y',
    'filing_date',
    'filing_date_x',
    'filing_date_y',
    'netIncome_y',
    'ticker_x',
    'ticker_y',
    'key'
]

# Datetime columns
datetime_cols = [
    'date',
    'filing_date',
    'filing_date_x',
    'filing_date_y'
    'full_filing_date',
    'alter_filing_date'
]

target_cols = [
    'y_1y'
]
