import pandas as pd

from services.utils import timeit
from settings import params


# Globals
DATA_DIRECTORY = params.DATA_DIRECTORY


@timeit
def open_reports(*args) -> pd.DataFrame:
    """
    Opens the required reports from the local storage.
    :param args: Names of reports
    :return: Pandas data frames
    """
    report = pd.DataFrame()
    for report_name in args:
        try:
            report = pd.read_parquet(f'{DATA_DIRECTORY}/{report_name}.parquet')
            print(f'Report {report_name} opened, count: {len(report)}')
            return report
        except KeyError:
            print(f'error: File {report_name} not found')
    return report


open_reports('Balance_Sheet_report', 'Cash_Flow_report', 'Income_Statement_report')
