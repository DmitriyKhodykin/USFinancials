"""
Data preparation module.
"""
import os
import zipfile
import pandas as pd


def unpack_data(data_dir='US_Financials') -> pd.DataFrame:
    """
    Unpacks a data archive and converts file links to dataframe
    :return: dataframe with links to files
    """
    z = zipfile.ZipFile('src_data.zip', 'r')
    z.extractall()

    files = []
    for i in os.listdir(data_dir):
        files.append([data_dir + '/' + i])

    df = pd.DataFrame(files, columns=['address'], index=None)
    start_ticker_name = len(data_dir)
    df['ticker'] = df['address'].apply(lambda x: x[start_ticker_name:-5])

    return df


if __name__ == '__main__':
    df = unpack_data()
    print(df.head())
