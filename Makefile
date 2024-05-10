SHELL := /bin/bash

.ONESHELL:

.DEFAULT_GOAL := help

.PHONY: help start start_build stop tests tests_local check_typing check_typing_local

TESTS = pytest tests/* -vv

help:
	@echo "Available targets:"
	@echo "  help      : Display this help message"
	@echo "  start     : Start the application"
	@echo "  start_dev : Start the application with dev profile"
	@echo "  start_build: Start the application with build"
	@echo "  start_build_dev: Start the application with build and dev profile"
	@echo "  stop      : Stop the application"
	@echo "  stop_dev  : Stop the application with dev profile"
	@echo "  tests     : Run the tests"
	@echo "  tests_local: Run the tests locally"
	@echo "  check_typing: Check the typing"
	@echo "  check_typing_local: Check the typing locally"
	@echo "  wheel	 : Create a wheel package"

start:
	@docker compose up -d

start_dev:
	@docker compose --profile dev up -d

start_build:
	@docker compose up -d --build

start_build_dev:
	@docker compose --profile dev up -d --build

stop:
	@docker compose down

stop_dev:
	@docker compose --profile dev down

tests:
	@docker compose exec -T inventory-app-tests $(TESTS)

tests_local:
	@$(TESTS)

check_typing:
	@docker compose exec -T inventory-app-tests mypy .

check_typing_local:
	@mypy .

#------------------------------------------------------------#

requirements.txt: poetry.lock
	@poetry export -f requirements.txt --output requirements.txt

requirements-dev.txt: poetry.lock
	@poetry export -f requirements.txt --output requirements-dev.txt --with dev

dist: requirements.txt requirements-dev.txt
	@poetry build

.PHONY: wheel
wheel: dist