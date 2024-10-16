API_NAME="ml-api"

# verifying which docker compose command is available
ifneq (, $(shell which docker-compose))
    DOCKER_COMPOSE = docker-compose
else ifneq (, $(shell which docker))
    DOCKER_COMPOSE = docker compose
else
    $(error "Neither docker-compose nor docker compose is available")
endif

############################################
# COMMANDS TO RUN USING DOCKER (RECOMMENDED)
############################################

docker/install: 
	$(DOCKER_COMPOSE) build ${API_NAME}

docker/lint:
	$(DOCKER_COMPOSE) run ${API_NAME} poetry run task lint

docker/test:
	$(DOCKER_COMPOSE) run ${API_NAME} poetry run task test

docker/model_dummy:
	$(DOCKER_COMPOSE) exec ${API_NAME} poetry run python model_dummy.py

docker/run:
	$(DOCKER_COMPOSE) up --build