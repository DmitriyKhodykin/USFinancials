"""
Main module for the raw data pipeline
"""
import pandas as pd

from . import (data_import, data_preparation,
               data_transformation, data_cleaning)


def main():
    """
    Main data pipeline.
    """
    # Preparation data
    data_preparation.unpack_data()
    links_dataset = pd.read_parquet('links.parquet')
    for branch_item in ['Balance_Sheet', 'Cash_Flow', 'Income_Statement']:
        data_preparation.create_financial_datasets(links_dataset, branch_item)

    # Import data
    data_import.get_unique_tickers_list()
    data_import.import_stock_quotes()
    data_import.import_index_500()

    # Transformation data
    data_transformation.percentage_change('SP500', 'Stock')
    data_transformation.joining_reports()
    data_transformation.create_target('StockRelative', 'RawData')


if __name__ == '__main__':
    main()
