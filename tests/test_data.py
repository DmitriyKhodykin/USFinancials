from unittest import TestCase

import pandas

from settings.params import reports

df = pandas.read_parquet(reports['RawData'])
print(df)


