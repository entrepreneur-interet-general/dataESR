import pymongo
import logging
from connector import ConnectorDatabase, ConfigDatabase

logger = logging.getLogger(__name__)

class MongoDatabase(ConnectorDatabase):
    def __init__(self, pathconfig, database):
        super(MongoDatabase, self).__init__(pathconfig)
        self.db = database
        try:
            self._connection()
        except:
            raise Exception('Failed to connect to mongo with params: {}'.format(self.params))

    def _connection(self):
        self.type_db = 'mongo'
        self.connection = pymongo.MongoClient(**self.params.get_config(section='mongo'))