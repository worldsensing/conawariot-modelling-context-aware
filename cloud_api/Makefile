VERSION=0.1.0
NAME=backend
DOCKER_NAME=$(NAME):$(VERSION)

.EXPORT_ALL_VARIABLES:

clean:
	@find . -iname "*~" | xargs rm 2>/dev/null || true
	@find . -iname "*.pyc" | xargs rm 2>/dev/null || true
	@find . -iname "build" | xargs rm -rf 2>/dev/null || true

build: clean
	docker compose build ${NAME}

start: build
	docker compose -f docker-compose.yml up --force-recreate --no-deps ${NAME}

setup:
	docker compose -f docker-compose.yml up --force-recreate --no-deps postgres pgadmin

stop:
	docker compose -f docker-compose.yml stop

test:
	pytest