"""
Unittests for data flow modules.
"""
from unittest import TestCase

import pandas

from settings.params import reports

df = pandas.read_parquet(reports['CleanData'])

for i in df.columns:
    print(i)
