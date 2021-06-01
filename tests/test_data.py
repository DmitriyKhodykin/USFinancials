from unittest import TestCase

import pandas

from settings import params

dir = params.RAW_DATA_DIRECTORY


df = pandas.read_parquet(f'{dir}/Balance_Sheet_Report.parquet')
print(df)
