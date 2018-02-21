"""
Test file for a first flow
"""

import os
from connector import ConnectorDatabase
from recipes import Datasets

def function_to_apply(dataset):
    pass

if __name__ == '__main__':
    path_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(path_dir, "config/example/database.ini")
    connector = ConnectorDatabase(filename)
    ds = Datasets(connector, "test", type='postgresql')
    print(ds.datasets.head())
