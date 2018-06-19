
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
run-worker:
	${DC} --name dataESR-airflow run worker
logs:
	${DC} logs --f
stop:
	${DC} down
clean: clean-images stop
	${DC} rm -f
clean-images:
	docker rmi -f dataesr_webserver dataesr_worker dataesr_flower dataesr_scheduler
relaunch: clean run