DC = docker compose

APP = docker_compose/app.yaml

REDIS = docker_compose/redis.yaml
MONGO = docker_compose/mongo.yaml

ENV = --env-file .env


.PHONY: app
app:
	${DC} -f ${APP} ${ENV} up -d --build

.PHONY: app-down
app-down:
	${DC} -f ${APP} ${ENV} down

.PHONY: storages
storages:
	${DC} -f ${MONGO} -f ${REDIS} ${ENV} up -d --build

.PHONY: storages-down
storages-down:
	${DC} -f ${MONGO} -f ${REDIS} ${ENV} down

.PHONY: all
all:
	${DC} -f ${APP} -f ${MONGO} -f ${REDIS} ${ENV} up -d --build

.PHONY: all-down
all-down:
	${DC} -f ${APP} -f ${MONGO} -f ${REDIS} ${ENV} down
