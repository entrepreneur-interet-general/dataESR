import pytest
import os
from mock import patch, Mock, MagicMock
from connector import ConnectorDatabase, MongoDatabase, PSQLDatabase

class TestConnector():
    """Testing connector for different type of database"""

    @patch("psycopg2.connect")
    def test_connector_psql(self, psqlconnect):
        path_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(path_dir, "testconfig/testdatabase.ini")
        psql_connection = PSQLDatabase(filename)
        psqlconnect.assert_called_with(**psql_connection.params.get_config(section='postgresql'))
        assert psql_connection.type_db == 'postgresql'
    
    @patch("pymongo.MongoClient")
    def test_connector_mongo(self, mongoconnect):
        path_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(path_dir, "testconfig/testdatabase.ini")
        mongo_connection = MongoDatabase(filename, database='test')
        mongoconnect.assert_called_with(**mongo_connection.params.get_config(section='mongo'))
        assert mongo_connection.type_db == 'mongo'
        
