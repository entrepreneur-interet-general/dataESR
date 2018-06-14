#!/bin/sh

set -e

echo '-----------------------------------'
echo '-----setting local environment-----'
echo '-----------------------------------'


echo 'exporting env. var'
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

echo 'Finished exporting var.\n'

echo 'Checking environnement'

for i in ${DISK_LOCATION} ${DATA_LOCATION} ${AIRFLOW_HOME} ${MONGO_VOLUME} ${POSTGRESQL_VOLUME}
    do 
        if [[ -z "${i}" ]]; then
            echo '$i is not set'
            exit 1
        fi
    done

echo 'Environment checked: all variables are set.\n'
