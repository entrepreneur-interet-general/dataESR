"""
Tagger
"""

from airflow import DAG
from datetime import datetime, timedelta
from mongo_plugin import MongoHook
from airflow.operators.python_operator import PythonOperator
from airflow.models import BaseOperator
import logging
from pymongo import MongoClient

MONGO_LOGIN = ''
MONGO_PASSWORD = ''
MONGO_CONN_ID = 'localhost'
MONGO_PORT = '27017'
MONGO_DB = 'wikipedia'
MONGO_COLLECTION = 'wiki_en'

mongo_uri = {
    'login': MONGO_LOGIN,
    'password': MONGO_PASSWORD,
    'host': MONGO_CONN_ID,
    'port': MONGO_PORT,
    'database': MONGO_DB
}

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now() + timedelta(minutes=1),
    'email': [],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    'tagger', default_args=default_args)

def check_mongo_db(**kwargs):
    mongo_uri = kwargs.get('mongo_uri')
    mongo_db = kwargs.get('mongo_db')
    mongo_collection = kwargs.get('mongo_collection')
    mongo_conn = MongoHook(mongo_uri).get_conn()
    # Grab collection
    collection = mongo_conn.get_database(mongo_db).get_collection(mongo_collection)

    count = collection.find().count()
    if  count > 0:
        logging.info('Total in mongo db: {}, coll: {}, count: {}'.format(mongo_db, mongo_collection, count))
        return True
    else:
        logging.info('No data found in mongo db: {}, coll: {}'.format(mongo_db, mongo_collection))
        return False
    
with dag:
    mongo = PythonOperator(task_id='check_mongo',
                           python_callable=check_mongo_db,
                           op_kwargs={"mongo_uri": mongo_uri,
                                   "mongo_db": MONGO_DB,
                                   "mongo_collection": MONGO_COLLECTION},
                           provide_context=True)