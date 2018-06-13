"""
wikipedia DAG
"""
from airflow import DAG
from datetime import datetime, timedelta


def check_wikipedia_db():
    pass


def fill_up_wikipedia_db():
    pass


def get_q_id():
    pass


def get_instances_subclasses():
    pass


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

with dag:
    pass
