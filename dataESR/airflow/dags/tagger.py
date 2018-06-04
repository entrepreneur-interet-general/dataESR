"""
Tagger
"""

from airflow import DAG
from datetime import datetime, timedelta
from mongo_plugin import MongoHook
from airflow.operators.python_operator import ShortCircuitOperator
import logging

MONGO_CONN_ID = 'localhost:27017'
MONGO_DB = 'wikipedia'
MONGO_COLLECTION = 'wiki_en'


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
    mongo_conn_id = kwargs.get('mongo_conn_id')
    mongo_db = kwargs.get('mongo_db')
    mongo_collection = kwargs.get('mongo_collection')

    mongo_conn = MongoHook(conn_id=mongo_conn_id).get_conn()

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
    mongo = ShortCircuitOperator(task_id='check_mongo',
                                 python_callable=check_mongo_db,
                                 op_kwargs={"mongo_conn_id": MONGO_CONN_ID,
                                            "mongo_db": MONGO_DB,
                                            "mongo_collection": MONGO_COLLECTION},
                                 provide_context=True)
