"""
Open Research Corpus DAG
"""

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator

PATH_DOWNLOAD = ''
PATH_DECOMPRESS = ''
URL = ''

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': [],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=2)
}

dag = DAG('openresearchcorpus', default_args=default_args)

with dag:
    download = BashOperator(
        bash_command='wget -P {{PATH_DOWNLOAD}} -i \
        https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/\
            manifest.txt',
        params={'PATH_DOWNLOAD': PATH_DOWNLOAD,
                'PATH_DECOMPRESS': PATH_DECOMPRESS}
    )
    decompress = BashOperator(
        bash_command='gzip -d {{PATH_DOWNLOAD}}/*.gz > {{PATH_DECOMPRESS}}'
    )
