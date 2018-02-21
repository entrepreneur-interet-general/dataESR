import logging
import psycopg2
from config.config import ConfigDatabase

class ConnectorDatabase(object):
    def __init__(self, pathconfig):
        self.params = ConfigDatabase(pathconfig)
        self.connection = None
        self.type_db = None

    def _connect_to_psql(self):
        """ Connect to psql database server """
        self.type_db = 'postgresql'
        conn = None
        try:
            # read connection parameters
            # connect to the PostgreSQL server
            logging.info('Connecting to the PostgreSQL database...')
            params = self.params.get_config(section="postgresql")
            self.connection = psycopg2.connect(**params)
            # create a cursor
            cur = self.connection.cursor()
        # execute a statement
            cur.execute('SELECT version()')
            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            logging.info('PostgreSQL database version: %s' %db_version)
         # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
