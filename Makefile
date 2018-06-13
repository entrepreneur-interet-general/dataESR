install:
	. install.sh
	@echo 'Installed complete.'

run-worker:
	docker-compose run worker