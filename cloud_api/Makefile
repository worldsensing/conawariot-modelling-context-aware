NAME=cloud_api_modelling_context_aware
VERSION=1.0.0-RC1
DOCKER_NAME=phd/$(NAME)
DOCKER_NAME_FULL=$(DOCKER_NAME):$(VERSION)

clean:
	@find . -iname "*~" | xargs rm 2>/dev/null || true
	@find . -iname "*.pyc" | xargs rm 2>/dev/null || true
	@find . -iname "build" | xargs rm -rf 2>/dev/null || true

build: clean
	docker build -f Dockerfile -t $(DOCKER_NAME_FULL) .

run: build
	docker-compose -f docker-compose.yml -p phd_deployment up -d

setup: build
	docker-compose -f docker-compose.yml -p phd_deployment up -d postgres

run-tests: build
	docker-compose -f docker-compose.test.yml -p phd_deployment_test up --build backend_demo_api_test

setup-tests: build
	docker-compose -f docker-compose.test.yml -p phd_deployment_test up -d postgres