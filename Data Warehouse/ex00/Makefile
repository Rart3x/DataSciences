NAME = db

all:
	@docker compose -f srcs/docker-compose.yml up -d --remove-orphans

down:
	@docker compose -f srcs/docker-compose.yml down

fclean:
	@docker system prune --all --force --volumes
	@docker network prune --force
	@docker volume prune --force
	@docker stop adminer db > /dev/null 2>&1 || true
	@docker rm adminer db > /dev/null 2>&1 || true

re: down all