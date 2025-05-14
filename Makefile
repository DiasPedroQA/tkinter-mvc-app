# =============================================
# VARIÁVEIS GLOBAIS
# =============================================
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

# =============================================
# TARGETS PHONY
# =============================================
.PHONY: help venv install update-deps \
        lint test coverage security mypy format \
        pre-commit-install pre-commit-run \
        run docker-build docker-run \
        clean all check-consistency

# =============================================
# AJUDA (target padrão)
# =============================================
help:
	@echo "\n\033[1mCOMANDOS DISPONÍVEIS PARA tkinter-mvc-app:\033[0m\n"
	@echo "\033[1mConfiguração:\033[0m"
	@echo "  install            Instala dependências de desenvolvimento"
	@echo "  update-deps        Atualiza dependências principais"
	@echo "\n\033[1mVerificação:\033[0m"
	@echo "  lint               Executa verificações de estilo (flake8 + pylint)"
	@echo "  test               Executa testes unitários"
	@echo "  coverage           Executa testes com cobertura"
	@echo "  security           Verifica vulnerabilidades com bandit"
	@echo "  mypy               Verificação estática de tipos"
	@echo "\n\033[1mFormatação:\033[0m"
	@echo "  format             Formata código (black + isort)"
	@echo "  pre-commit-install Instala hooks do pre-commit"
	@echo "  pre-commit-run     Executa pre-commit em todos os arquivos"
	@echo "\n\033[1mExecução:\033[0m"
	@echo "  run                Executa a aplicação principal"
	@echo "  docker-build       Constrói a imagem Docker"
	@echo "  docker-run         Executa o container Docker"
	@echo "\n\033[1mUtilitários:\033[0m"
	@echo "  clean              Remove arquivos temporários"
	@echo "  check-consistency  Verifica consistência entre pre-commit e requirements"
	@echo "  all                Executa clean, install, test e run\n"

# =============================================
# CONFIGURAÇÃO DE AMBIENTE
# =============================================
venv:
	@echo "\033[1mCriando ambiente virtual...\033[0m"
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(PYTHON) -m pip install --upgrade pip wheel

install: venv
	@echo "\033[1mInstalando dependências...\033[0m"
	@$(PIP) install -r requirements-dev.txt

update-deps: venv
	@echo "\033[1mAtualizando dependências...\033[0m"
	@$(PIP) install --upgrade -r requirements.txt

# =============================================
# VERIFICAÇÕES DE CÓDIGO
# =============================================
lint:
	@echo "\033[1mExecutando verificações de código...\033[0m"
	@echo "\n\033[1;34m=== Flake8 ===\033[0m"
	@$(PYTHON) -m flake8 --config $(CONFIG_DIR)/.flake8 $(SRC_DIR)
	@echo "\n\033[1;34m=== Pylint ===\033[0m"
	@$(PYTHON) -m pylint --rcfile $(CONFIG_DIR)/.pylintrc $(SRC_DIR)

test:
	@echo "\033[1mExecutando testes...\033[0m"
	@$(PYTHON) -m pytest -c $(CONFIG_DIR)/pytest.ini $(TEST_DIR)

coverage: venv
	@echo "\033[1mExecutando testes com cobertura...\033[0m"
	@$(PYTHON) -m pytest --cov=$(SRC_DIR) --cov-report=term --cov-report=html -c $(CONFIG_DIR)/pytest.ini

security: venv
	@echo "\033[1mVerificando segurança com bandit...\033[0m"
	@$(PYTHON) -m bandit -r $(SRC_DIR) -c $(CONFIG_DIR)/bandit.yml

mypy: venv
	@echo "\033[1mVerificando tipos com mypy...\033[0m"
	@$(PYTHON) -m mypy $(SRC_DIR) --config-file $(CONFIG_DIR)/pyproject.toml

# =============================================
# FORMATAÇÃO
# =============================================
format: venv
	@echo "\033[1mFormatando código...\033[0m"
	@echo "\n\033[1;34m=== Black ===\033[0m"
	@$(PYTHON) -m black .
	@echo "\n\033[1;34m=== isort ===\033[0m"
	@$(PYTHON) -m isort .

# =============================================
# PRE-COMMIT
# =============================================
pre-commit-install: venv
	@echo "\033[1mConfigurando pre-commit...\033[0m"
	@$(PRECOMMIT) autoupdate || echo "\033[33mAutoupdate opcional falhou, continuando...\033[0m"
	@$(PRECOMMIT) install --config $(CONFIG_DIR)/../pre-commit/.pre-commit-config.yaml
	@$(PRECOMMIT) install-hooks

pre-commit-run: pre-commit-install
	@echo "\033[1mExecutando pre-commit...\033[0m"
	@$(PRECOMMIT) run --all-files --config $(CONFIG_DIR)/../pre-commit/.pre-commit-config.yaml

# =============================================
# EXECUÇÃO
# =============================================
run: venv
	@echo "\033[1mIniciando aplicação...\033[0m"
	@$(PYTHON) $(SRC_DIR)/main.py

docker-build:
	@echo "\033[1mConstruindo imagem Docker...\033[0m"
	@docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

docker-run:
	@echo "\033[1mExecutando container...\033[0m"
	@docker run -p $(PORT):$(PORT) $(DOCKER_IMAGE):$(DOCKER_TAG)

# =============================================
# UTILITÁRIOS
# =============================================
clean:
	@echo "\033[1mLimpando arquivos temporários...\033[0m"
	@rm -rf \
		.pytest_cache \
		__pycache__ \
		.coverage \
		htmlcov \
		build \
		dist \
		*.egg-info \
		$(VENV)

check-consistency: venv
	@echo "\033[1mVerificando consistência de versões...\033[0m"
	@echo "\n\033[1;34m=== Pre-commit ===\033[0m"
	@$(PYTHON) -c "import tomli; config = tomli.load(open('$(CONFIG_DIR)/../pre-commit/.pre-commit-config.yaml', 'rb')); print('\n'.join(f'{hook['id']}: {repo['rev']}' for repo in config['repos'] for hook in repo['hooks']))"
	@echo "\n\033[1;34m=== Ambiente ===\033[0m"
	@$(PIP) freeze | grep -E 'black|isort|flake8|mypy|bandit|pytest' || echo "Nenhuma dependência relevante instalada"

# =============================================
# META-TARGET
# =============================================
all: clean install test run
