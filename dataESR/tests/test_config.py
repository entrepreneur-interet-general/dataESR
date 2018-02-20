import unittest
from config.config import ConfigDatabase
import ConfigParser
import os

class TestConfigDatabase(unittest.TestCase):
    def test_config_database(self):
        path_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(path_dir, "testconfig/testdatabase.ini")
        self.assertEquals(
            ConfigDatabase(filename).config_dbs,
            {
                'postgresql': {
                    "host": "localhost",
                    "database": "db",
                    "user": "postgres",
                    "password": "postgres"
                }
            }
        )
