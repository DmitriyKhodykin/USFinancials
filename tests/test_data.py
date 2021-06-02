from unittest import TestCase

import pandas

from settings.params import reports

df = pandas.read_parquet(reports['RawData'])
for i in df.columns:
    print(i)


