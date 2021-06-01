from unittest import TestCase

import pandas

from settings import params

dir = params.DATA_DIRECTORY


df = pandas.read_parquet(f'{dir}/Index_500.parquet')
print(df)
