import psycopg2
import pandas as pd
from config.config import ConfigDatabase

class ConnectorDatabase(object):
    def __init__(self, pathconfig):
        self.params = ConfigDatabase(pathconfig)
        self.connection = None
        self.type_db = None