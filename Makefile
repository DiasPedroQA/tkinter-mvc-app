.PHONY: install test run clean all lint mypy pre-commit coverage format security docker-build docker-run update-deps venv

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PRECOMMIT := $(VENV)/bin/pre-commit
SRC_DIR = src
TEST_DIR = tests

# Garante que o venv exista
venv:
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)

install:
	$(PIP) install -r requirements.txt

test: venv
	$(VENV_DIR)/bin/pytest $(TEST_DIR)

lint: venv
	$(VENV_DIR)/bin/black .
	$(VENV_DIR)/bin/isort .
	$(VENV_DIR)/bin/flake8

mypy: venv
	$(VENV_DIR)/bin/mypy $(SRC_DIR)

pre-commit:
	$(PRECOMMIT) install
	$(PRECOMMIT) run --all-files

coverage: venv
	$(VENV_DIR)/bin/pytest --cov=$(SRC_DIR) --cov-report=term --cov-report=html

format: venv
	$(VENV_DIR)/bin/black .
	$(VENV_DIR)/bin/isort .

security: venv
	$(VENV_DIR)/bin/bandit -r $(SRC_DIR)

run: venv
	$(PYTHON) $(SRC_DIR)/main.py

all: clean install test run

clean:
	@echo "Removendo arquivos temporários..."
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf .coverage
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf logs
	rm -rf $(VENV_DIR)

docker-build:
	docker build -t tkinter-mvc-app .

docker-run:
	docker run -p 8000:8000 tkinter-mvc-app

update-deps: venv
	$(PIP) install --upgrade -r requirements.txt
