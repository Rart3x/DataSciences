NAME = db

all:
	@docker compose -f srcs/docker-compose.yml up

down:
	@docker compose -f srcs/docker-compose.yml down

fclean: down
	@docker system prune --all --force --volumes
	@docker network prune --force
	@docker volume prune --force
	@rm -rf ./srcs/services/db/db-data ./srcs/services/adminer/adminer-data ./srcs/services/python-runner/python-runner-data

re: down all