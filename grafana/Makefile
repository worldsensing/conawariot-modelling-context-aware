NAME=grafana
DOCKER_NAME=phd/$(NAME)
VERSION=1.0.0-RC1
DOCKER_NAME_FULL=$(DOCKER_NAME):$(VERSION)
DOCKER_LOCALHOST=$(shell /sbin/ip addr show docker0 | grep -Po 'inet \K[\d.]+')

clean:
	@find . -iname "*~" | xargs rm 2>/dev/null || true
	@find . -iname "*.pyc" | xargs rm 2>/dev/null || true
	@find . -iname "build" | xargs rm -rf 2>/dev/null || true

build: clean
	docker build -t $(DOCKER_NAME_FULL) .

run: build
	docker run -it -p 3001:3000 \
		--add-host postgres:$(DOCKER_LOCALHOST) \
		--name $(NAME) \
		--volume $(shell pwd)/ENV/grafana.ini:/etc/grafana/grafana.ini \
		--env-file ENV/grafana.env \
		--rm $(DOCKER_NAME_FULL)

setup:
	docker-compose -f docker-compose.yml up -d postgres