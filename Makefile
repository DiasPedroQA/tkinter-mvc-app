.PHONY: install test run clean all lint mypy pre-commit coverage format security docker-build docker-run update-deps

PYTHON = python
PIP = pip
SRC_DIR = src
TEST_DIR = tests

install:
	$(PIP) install -r requirements.txt

test:
	pytest $(TEST_DIR)

lint:
	black . && isort . && flake8

mypy:
	mypy $(SRC_DIR)

pre-commit:
	pre-commit install

coverage:
	pytest --cov=$(SRC_DIR) --cov-report=term --cov-report=html

format:
	black . && isort .

security:
	bandit -r $(SRC_DIR)

run:
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

docker-build:
	docker build -t tkinter-mvc-app .

docker-run:
	docker run -p 8000:8000 tkinter-mvc-app

update-deps:
	$(PIP) install --upgrade -r requirements.txt
