import pandas as pd

class Datasets(object):
    """ Format a dataset from the import of database connector"""

    def __init__(self, connector, table, columns=None, type=None):
        self.table = table
        self.connector = connector
        self.datasets = self.connector.extract_df(type, table=self.table, columns=columns)
        self.columns = column

    def apply_recipes(self):
        pass

    def dump_dataset(self, conf):
        pass

class Recipe(Datasets):
    """ A recipe is an action to perform to a specific dataframe"""
    def __init__(self, input, action):
        self.input = input
        self.action = action
    def apply_recipe(self):
        return self.input.apply(action)

class Recipes(Recipe):
    def __init__(self, name=None, recipes=[]):
        self.name = name
        self.input = Datasets.datasets
        self.recipes = recipes

    def run(self):
        for r in self.recipes:
            r.input.apply_recipe()
