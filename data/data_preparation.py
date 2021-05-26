"""
Data preparation module.
"""
import json
import os
import zipfile
import pandas as pd


def unpack_data(data_dir='US_Financials') -> None:
    """
    Unpacks a data source archive and save links to files in parquet.
    :return: None
    """
    z = zipfile.ZipFile('src_data.zip', 'r')
    z.extractall()

    files = []
    for i in os.listdir(data_dir):
        files.append([data_dir + '/' + i])

    data = pd.DataFrame(files, columns=['address'], index=None)
    start_ticker_name = len(data_dir) + 1
    end_ticker_name = -5
    data['ticker'] = data['address'].apply(lambda x: x[start_ticker_name:end_ticker_name])
    data.to_parquet('links.parquet')


def create_financial_datasets(links: pd.DataFrame, branch: str) -> None:
    """
    Create and save data sets with financials indicators.
    :param links: data frame with links to json files
    :param branch: type of financial report
    :return: None
    """
    dataset: pd.DataFrame = pd.DataFrame()

    # Iterating for all JSON's
    for index, row in links.iterrows():
        address = row['address']
        try:
            with open(address, "r") as content:
                tmp_dict = json.load(content)

            sheet = pd.DataFrame(
                tmp_dict['Financials'][branch]['quarterly']  # Only quarterly reports
            ).T  # Transpose sheet

            sheet['ticker'] = row['ticker']
            sheet['filing_date'] = pd.to_datetime(sheet['filing_date'])
            sheet['date'] = pd.to_datetime(sheet['date'])
            dataset = dataset.append(sheet)
        except (KeyError, UnicodeDecodeError):
            pass

    dataset.to_parquet(f'{branch}_report.parquet')


if __name__ == '__main__':
    unpack_data()
    links_dataset = pd.read_parquet('links.parquet')
    for branch_item in ['Balance_Sheet', 'Cash_Flow', 'Income_Statement']:
        create_financial_datasets(links_dataset, branch_item)
