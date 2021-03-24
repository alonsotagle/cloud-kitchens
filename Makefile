
##########################
#          Build         #
##########################

build:
	@cd infra && docker-compose -f docker-compose.build.yml up -d


##########################
#          Start         #
##########################

start:
	@docker-compose -f infra/docker-compose.start.yml down
	@cd infra && docker-compose -f docker-compose.start.yml up -d


##########################
#          Stop          #
##########################
stop:
	@docker-compose -f infra/docker-compose.build.yml down
	@docker-compose -f infra/docker-compose.start.yml down


##########################
#         Testing        #
##########################

tests:
	@echo "Testing"
	@make tests
