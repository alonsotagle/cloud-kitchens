
##########################
#          Build         #
##########################

build:
	@docker-compose -f infra/docker-compose.build.yml up -d


##########################
#          Start         #
##########################

start:
	@docker-compose -f infra/docker-compose.start.yml down
	@docker-compose -f infra/docker-compose.start.yml up -d


##########################
#          Stop          #
##########################
stop:
	@docker-compose -f infra/docker-compose.build.yml down
	@docker-compose -f infra/docker-compose.start.yml down


##########################
#         Testing        #
##########################

run-tests:
	@docker-compose -f infra/docker-compose.tests.yml up -d
