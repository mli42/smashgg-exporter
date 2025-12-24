NAME := smashgg-exporter-postgres
DOCKER := docker
DC := docker compose

DOCKER_EXEC := $(DOCKER) exec -it $(NAME)

all: up

up:
	$(DC) up --build

sh:
	$(DOCKER_EXEC) bash

re: fclean all

reload: down all

logs:
	$(DC) logs --follow --tail 1000

stop:
	$(DC) stop

down:
	$(DC) down

ps:
	$(DC) ps

clean:
	$(DC) down --rmi all

fclean:
	$(DC) down --rmi all --volumes
