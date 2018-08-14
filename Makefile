
export DISK_LOCATION=/mnt/disk1
export DATA_LOCATION=${DISK_LOCATION}/data

dbs = mongo psql

export AIRFLOW_HOME=${DISK_LOCATION}/dataESR/airflow
export MONGO_VOLUME=${DATA_LOCATION}/mongo
export POSTGRESQL_VOLUME=${DATA_LOCATION}/psql

export http_proxy=
export https_proxy=

DC := 'docker-compose'

create-env:
	$(foreach i, $(dbs), sudo mkdir -p $(DATA_LOCATION)/$i)
build:
	${DC} up -d 
install: create-env build
run-worker-airflow:
	${DC} run -d airflow-worker
run-airflow: run-worker-airflow
logs:
	${DC} logs --f
stop:
	${DC} down
clean: clean-images stop
	${DC} rm -f
clean-images:
	docker rmi -f dataesr_airflow-webserver \
		dataesr_airflow-worker \
		dataesr_airflow-flower \
		dataesr_airflow-scheduler
relaunch: clean run