
export DISK_LOCATION=/mnt/disk1
export DATA_LOCATION=${DISK_LOCATION}/data

dbs = mongo psql

export AIRFLOW_HOME=${DISK_LOCATION}/dataESR/airflow
export MONGO_VOLUME=${DATA_LOCATION}/mongo
export POSTGRESQL_VOLUME=${DATA_LOCATION}/psql

DC := 'docker-compose'

install:
	$(foreach i, $(dbs), @sudo mkdir -p $(DATA_LOCATION)/$i)
up:
	${DC} up
run: install up
	${DC} run worker
logs:
	@docker logs