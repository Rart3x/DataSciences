NAME = db

all:
	@docker compose -f srcs/docker-compose.yml up -d

down:
	@docker compose -f srcs/docker-compose.yml down

fclean: down
	@docker system prune --all --force --volumes
	@docker network prune --force
	@docker volume prune --force

re: down all