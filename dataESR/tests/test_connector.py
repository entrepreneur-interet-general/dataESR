import unittest
import os
from mock import patch, Mock, MagicMock
from connector import ConnectorDatabase

class TestConnector(unittest.TestCase):
    """Testing connector for different type of database"""

    @patch("psycopg2.connect")
    def test_connector_psql(self, psqlconnect):
        path_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(path_dir, "testconfig/testdatabase.ini")
        connector = ConnectorDatabase(filename)
        connector._connect_to_psql()
        psqlconnect.assert_called_with(**connector.params.get_config(section='postgresql'))
        self.assertEquals(connector.type_db, 'postgresql')
