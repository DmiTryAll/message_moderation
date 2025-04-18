DC = docker compose

APP = docker_compose/app.yaml

REDIS = docker_compose/redis.yaml
MONGO = docker_compose/mongo.yaml
POSTGRESQL = docker_compose/postgresql.yaml

ENV = --env-file .env


.PHONY: run
run:
	python src/application/main.py

.PHONY: postgres
postgres:
	${DC} -f ${POSTGRESQL} ${ENV} up -d --build

.PHONY: postgres-down
postgres-down:
	${DC} -f ${POSTGRESQL} ${ENV} down

.PHONY: storages
storages:
	${DC} -f ${MONGO} -f ${POSTGRESQL} -f ${REDIS} ${ENV} up -d --build

.PHONY: storages-down
storages-down:
	${DC} -f ${MONGO} -f ${POSTGRESQL} -f ${REDIS} ${ENV} down
