# Variáveis
CONFIG_DIR := .config/development
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PRECOMMIT := $(VENV)/bin/pre-commit
SRC_DIR := src
TEST_DIR := tests
DOCKER_IMAGE := tkinter-mvc-app
DOCKER_TAG := latest
PORT := 8000

# Targets PHONY
.PHONY: venv install update-deps \
        lint test coverage security mypy format \
        pre-commit-install pre-commit-run \
        run \
        docker-build docker-run \
        clean help

# Ajuda (primeiro target, executado por padrão com 'make')
help:
	@echo "\nComandos disponíveis para tkinter-mvc-app:\n"
	@echo "  install            Instala dependências de desenvolvimento"
	@echo "  update-deps        Atualiza dependências principais"
	@echo "  lint               Executa verificações de estilo (flake8 + pylint)"
	@echo "  test               Executa testes unitários"
	@echo "  coverage           Executa testes com cobertura"
	@echo "  security           Verifica vulnerabilidades de segurança com bandit"
	@echo "  mypy               Verificação estática de tipos"
	@echo "  format             Formata código automaticamente (black + isort)"
	@echo "  pre-commit-install Instala hooks do pre-commit"
	@echo "  pre-commit-run     Executa pre-commit em todos os arquivos"
	@echo "  run                Executa a aplicação principal"
	@echo "  docker-build       Constrói a imagem Docker"
	@echo "  docker-run         Executa o container Docker"
	@echo "  clean              Remove arquivos temporários"
	@echo "  all                Executa clean, install, test e run\n"

# Configuração de ambiente
venv:
	@echo "Criando ambiente virtual..."
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(PYTHON) -m pip install --upgrade pip

install: venv
	@echo "Instalando dependências..."
	@$(PIP) install -r requirements-dev.txt

update-deps: venv
	@echo "Atualizando dependências..."
	@$(PIP) install --upgrade -r requirements.txt

# Verificações de código
lint:
	@echo "Executando flake8..."
	@$(PYTHON) -m flake8 --config $(CONFIG_DIR)/.flake8 $(SRC_DIR)
	@echo "\nExecutando pylint..."
	@$(PYTHON) -m pylint --rcfile $(CONFIG_DIR)/.pylintrc $(SRC_DIR)

test:
	@echo "Executando testes..."
	@$(PYTHON) -m pytest -c $(CONFIG_DIR)/pytest.ini $(TEST_DIR)

coverage: venv
	@echo "Executando testes com cobertura..."
	@$(PYTHON) -m pytest --cov=$(SRC_DIR) --cov-report=term --cov-report=html -c $(CONFIG_DIR)/pytest.ini

security: venv
	@echo "Verificando segurança com bandit..."
	@$(PYTHON) -m bandit -r $(SRC_DIR)

mypy: venv
	@echo "Verificando tipos com mypy..."
	@$(PYTHON) -m mypy $(SRC_DIR)

format: venv
	@echo "Formatando código com black..."
	@$(PYTHON) -m black .
	@echo "\nOrganizando imports com isort..."
	@$(PYTHON) -m isort .

# Pre-commit
pre-commit-install: venv
	@echo "Instalando hooks do pre-commit..."
	@$(PRECOMMIT) install --config $(CONFIG_DIR)/../pre-commit/.pre-commit-config.yaml

pre-commit-run: venv
	@echo "Executando pre-commit..."
	@$(PRECOMMIT) run --all-files --config $(CONFIG_DIR)/../pre-commit/.pre-commit-config.yaml

# Execução
run: venv
	@echo "Iniciando aplicação..."
	@$(PYTHON) $(SRC_DIR)/main.py

# Docker
docker-build:
	@echo "Construindo imagem Docker..."
	@docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

docker-run:
	@echo "Executando container..."
	@docker run -p $(PORT):$(PORT) $(DOCKER_IMAGE):$(DOCKER_TAG)

# Limpeza
clean:
	@echo "Limpando arquivos temporários..."
	@rm -rf \
		.pytest_cache \
		__pycache__ \
		.coverage \
		htmlcov \
		build \
		dist \
		*.egg-info \
		$(VENV)

# Meta-target
all: clean install test run
