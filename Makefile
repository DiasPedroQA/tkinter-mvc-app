.PHONY: install run test

# Variáveis
VENV_PATH=venv
VENV_ACTIVATE=$(VENV_PATH)/bin/activate
PYTHON=$(VENV_PATH)/bin/python
PIP=$(VENV_PATH)/bin/pip
COVERAGE=$(VENV_PATH)/bin/coverage

# Fase de instalação
install:
	@echo "Verificando se o ambiente virtual está ativado..."
	@if [ ! -d "$(VENV_PATH)" ]; then \
		echo "Ambiente virtual não encontrado. Criando o ambiente virtual..."; \
		python3 -m venv $(VENV_PATH); \
	fi
	@echo "Instalando as dependências..."
	@source $(VENV_ACTIVATE) && pip install -r requirements.txt
	@echo "Dependências instaladas com sucesso."

# Fase de execução do app
run:
	@echo "Verificando se o arquivo principal app/main.py existe..."
	@if [ ! -f "app/main.py" ]; then \
		echo "Erro: O arquivo app/main.py não foi encontrado."; \
		exit 1; \
	fi
	@echo "Executando o app..."
	@source $(VENV_ACTIVATE) && python app/main.py
	@if [ $$? -eq 0 ]; then \
		echo "App executado com sucesso."; \
	else \
		echo "Erro ao executar o app."; \
		exit 1; \
	fi
	@echo "App finalizado."

# Fase de execução dos testes
test:
	@echo "Verificando se o diretório de testes existe..."
	@if [ ! -d "tests" ]; then \
		echo "Erro: O diretório de testes não foi encontrado."; \
		exit 1; \
	fi
	@echo "Executando os testes..."
	@source $(VENV_ACTIVATE) && pytest tests/
	@if [ $$? -eq 0 ]; then \
		echo "Todos os testes passaram com sucesso."; \
	else \
		echo "Alguns testes falharam."; \
		exit 1; \
	fi

# Fase de cobertura de código
coverage:
	@echo "Verificando a cobertura de código..."
	@source $(VENV_ACTIVATE) && $(COVERAGE) run -m pytest tests/
	@source $(VENV_ACTIVATE) && $(COVERAGE) report -m
	@source $(VENV_ACTIVATE) && $(COVERAGE) html
	@echo "Cobertura de código verificada com sucesso."
	@echo "Relatório de cobertura gerado em htmlcov/index.html."
	@echo "Para visualizar o relatório de cobertura, abra o arquivo htmlcov/index.html em um navegador."
	@echo "Para visualizar o relatório de cobertura em formato de texto, execute: coverage report -m"
	@echo "Para visualizar o relatório de cobertura em formato HTML, execute: coverage html"
