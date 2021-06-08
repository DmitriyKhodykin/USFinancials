"""
Unittests for data flow modules.
"""
from unittest import TestCase

import pandas

from settings.params import reports

pd = pandas.read_parquet(reports['FeaturesData'])

for i in pd.iterrows():
    print(i)
