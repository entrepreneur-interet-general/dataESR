#!/bin/sh
echo '-----------------------------------'
echo '-----setting local environment-----'
echo '-----------------------------------'


export DISK_LOCATION=/mnt/disk1
export DATA_LOCATION=$DISK_LOCATION/data

dbs="mongo psql"

for i in $dbs; do
    echo $DATA_LOCATION/$i
    sudo mkdir -p $DATA_LOCATION/$i
done

export AIRFLOW_HOME=$DISK_LOCATION/dataESR/airflow
export MONGO_VOLUME=$DATA_LOCATION/mongo
export POSTGRESQL_VOLUME=$DATA_LOCATION/psql

echo 'Finished exporting var.'