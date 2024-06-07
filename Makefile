SHELL := /bin/bash

.ONESHELL:

.DEFAULT_GOAL := help

.PHONY: help start start_build start_dev start_build_dev stop tests tests_local check_typing check_typing_local

TESTS = pytest tests/* -vv
CHECK_LINT=/bin/sh -c "mypy . && isort --check-only . && black --check . && flake8 inventory_app models tests main.py"

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
	@echo "  jupyterlab: Run jupyterlab"
	@echo "  wheel	 : Create a wheel package"

.PHONY: .env
.env:
	@source .db-env/dbui.env
	@sed -i -E "s#DB_UI_inventory_db=.*#DB_UI_inventory_db=$$DB_UI_inventory_db#g" .env

start:
	@docker compose up -d
	$(MAKE) .env

start_dev:
	@docker compose --profile dev up -d
	$(MAKE) .env

start_build:
	@docker compose up -d --build
	$(MAKE) .env

start_build_dev:
	@docker compose --profile dev up -d --build
	$(MAKE) .env

stop:
	@docker compose down

stop_dev:
	@docker compose --profile dev down

tests:
	@docker compose exec -T inventory-app-dev $(TESTS)

tests_local:
	@$(TESTS)

check_lint:
	@docker compose exec inventory-app-dev mypy .
	@docker compose exec inventory-app-dev isort --check-only .
	@docker compose exec inventory-app-dev black --check .
	@docker compose exec inventory-app-dev flake8 inventory_app models tests main.py

check_lint_local:
	mypy . && isort --check-only . && black --check . && flake8 inventory_app models tests main.py

fix_lint:
	@docker compose exec inventory-app-dev isort .
	@docker compose exec inventory-app-dev black .

jupyterlab:
	@docker compose exec inventory-app-dev jupyter-lab --NotebookApp.token='' --no-browser --ip=0.0.0.0 --port=8888

#------------------------------------------------------------#

requirements.txt: poetry.lock
	@poetry export -f requirements.txt --output requirements.txt

requirements-dev.txt: poetry.lock
	@poetry export -f requirements.txt --output requirements-dev.txt --with dev

dist: requirements.txt requirements-dev.txt
	@poetry build

.PHONY: wheel
wheel: dist
