"""
Main module for the raw data pipeline
"""
import pandas as pd

from data import data_preparation, data_import, data_transformation
from data.data_cleaning import CleaningData
from settings import config
from settings.config import reports


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

    # Cleaning data
    cd = CleaningData(pd.read_parquet(reports['RawData']))
    cd.delete_extra_cols(config.extra_cols)
    cd.delete_rows_without_target(config.target_cols[0])
    cd.delete_empty_cols()
    cd.filling_missing_data()
    cd.delete_empty_rows()
    cd.cols_to_datetime(config.datetime_cols)
    cd.save_data()


if __name__ == '__main__':
    main()
