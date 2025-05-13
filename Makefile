.PHONY: install test run clean all lint mypy pre-commit coverage format security docker-build docker-run update-deps venv

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PRECOMMIT := $(VENV)/bin/pre-commit
SRC_DIR := src
TEST_DIR := tests

# Garante que o venv exista
venv:
	@test -d $(VENV) || python3 -m venv $(VENV)

install: venv
	$(PIP) install -r requirements.txt

test: venv
	$(VENV)/bin/pytest $(TEST_DIR)

lint: venv
	$(VENV)/bin/black .
	$(VENV)/bin/isort .
	$(VENV)/bin/flake8

mypy: venv
	$(VENV)/bin/mypy $(SRC_DIR)

pre-commit: venv
	$(PRECOMMIT) install
	$(PRECOMMIT) run --all-files

coverage: venv
	$(VENV)/bin/pytest --cov=$(SRC_DIR) --cov-report=term --cov-report=html

format: venv
	$(VENV)/bin/black .
	$(VENV)/bin/isort .

security: venv
	$(VENV)/bin/bandit -r $(SRC_DIR)

run: venv
	$(PYTHON) $(SRC_DIR)/main.py

all: clean install test run

clean:
	@echo "Removendo arquivos temporários..."
	rm -rf .pytest_cache __pycache__ .coverage build dist *.egg-info logs $(VENV)

docker-build:
	docker build -t tkinter-mvc-app .

docker-run:
	docker run -p 8000:8000 tkinter-mvc-app

update-deps: venv
	$(PIP) install --upgrade -r requirements.txt
