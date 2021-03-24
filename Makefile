WSL_DOCKER := $(shell command -v docker.exe 2> /dev/null)

ifdef WSL_DOCKER
DOCKER_COMPOSE := docker-compose.exe
else
DOCKER_COMPOSE := docker-compose
endif

##########################
#          Build         #
##########################

build:
	@$(DOCKER_COMPOSE) -f infra/docker-compose.build.yml up -d


##########################
#          Start         #
##########################

start:
	@$(DOCKER_COMPOSE) -f infra/docker-compose.start.yml down
	@$(DOCKER_COMPOSE) -f infra/docker-compose.start.yml up -d
	@$(DOCKER_COMPOSE) -f infra/docker-compose.start.yml logs -f kitchen


##########################
#         Testing        #
##########################

run-tests:
	@$(DOCKER_COMPOSE) -f infra/docker-compose.tests.yml up -d
	@$(DOCKER_COMPOSE) -f infra/docker-compose.tests.yml logs -f tests


##########################
#          Stop          #
##########################
stop:
	@$(DOCKER_COMPOSE) -f infra/docker-compose.build.yml down
	@$(DOCKER_COMPOSE) -f infra/docker-compose.start.yml down
	@$(DOCKER_COMPOSE) -f infra/docker-compose.tests.yml down
