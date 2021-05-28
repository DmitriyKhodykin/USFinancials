import pandas as pd

from services.utils import timeit


@timeit
def open_reports(rep1, rep2, rep3):
    bs_dataset = pd.read_parquet(f'{data_directory}/{rep1}.parquet')
    print('Balance_Sheet', len(bs_dataset), 'str')
    print(bs_dataset.head())

    cf_dataset = pd.read_parquet(f'{data_directory}/{rep2}.parquet')
    print('Cash_Flow', len(cf_dataset), 'str')
    print(cf_dataset.head())

    is_dataset = pd.read_parquet(f'{data_directory}/{rep3}.parquet')
    print('Income_Statement', len(is_dataset), 'str')
    print(is_dataset.head())


open_reports('Balance_Sheet_report', 'Cash_Flow_report', 'Income_Statement_report')