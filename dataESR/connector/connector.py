import logging
#from config import ConfigDatabase

class ConnectorDatabase(object):
    def __init__(self, pathconfig=None):
        self.params = ConfigDatabase(pathconfig)
        self.connection = None

    def _connect_to_psql(self):
        """ Connect to psql database server """
        conn = None
        try:
            # read connection parameters
            # connect to the PostgreSQL server
            logging.info('Connecting to the PostgreSQL database...')
            self.connection = psycopg2.connect(**self.params)
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
