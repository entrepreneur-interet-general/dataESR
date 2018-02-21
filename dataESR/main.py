"""
Test file for a first flow

Current simple flow is :

Connector >> Datasets >> Recipe >> Recipes 

"""

import os
from connector import ConnectorDatabase
from recipes import Datasets

def function_to_apply(dataset):
    """Take as an input a dataset, make relevant
    changes and return a new dataset"""
    pass

if __name__ == '__main__':

    path_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(path_dir, "config/example/database.ini")
    connector = ConnectorDatabase(filename)
    ds = Datasets(connector, "test", type='postgresql')
    print(ds.datasets.head())
