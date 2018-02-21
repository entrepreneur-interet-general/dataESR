import unittest
import ConfigParser
import os
from config.config import ConfigDatabase

class TestConfigDatabase(unittest.TestCase):
    def test_config_database(self):
        path_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(path_dir, "testconfig/testdatabase.ini")
        self.assertEquals(
            ConfigDatabase(filename).get_config(section="postgresql"),
            {
                "host": "localhost",
                "database": "db",
                "user": "postgres",
                "password": "postgres"
            }
        )
