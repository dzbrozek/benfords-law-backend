.PHONY : build
# Build docker image
build:
	docker build -t benfords-law-backend \
	--build-arg USER_ID=$(shell id -u) \
	--build-arg GROUP_ID=$(shell id -g) \
	$(arguments) .

.PHONY : up
# Start project
up:
	docker-compose up -d $(arguments)

.PHONY : bootstrap
# Bootstrap project
bootstrap: down removevolumes
	docker-compose run --rm backend bootstrap
	make up

.PHONY : down
# Stop project
down:
	docker-compose down --remove-orphans

.PHONY : removevolumes
removevolumes: down
	-docker volume rm `docker volume ls -f name=benfords-law -q|grep -v "pycharm"`

.PHONY : mypy
# Run mypy
mypy:
	docker-compose exec -T backend mypy --config-file ../mypy.ini ./

.PHONY : test
# Run tests
test:
	docker-compose exec backend python manage.py test $(arguments) --verbosity 3 --parallel

.PHONY : managepy
# Run manage.py
managepy:
	docker-compose exec -T backend python manage.py $(arguments)

.PHONY : precommit
# Run all pre-commit checks
precommit:
	pre-commit run --all-files

.PHONY : testci
# Test CI
testci:
	act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 --env-file "no-default-env-file" $(arguments)

.PHONY : status
# List Docker containers
status:
	docker-compose ps

.PHONY : help
# Show help
help:
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t


.DEFAULT_GOAL := help
