"""
Unittests for data flow modules.
"""
from unittest import TestCase

import pandas

from settings.config import reports

data = pandas.read_parquet(reports['FeaturesData'])

print(data)
