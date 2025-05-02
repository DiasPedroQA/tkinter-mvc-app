# Usar Bash para consistência
SHELL := /bin/bash

.PHONY: help install run test coverage lint clean all

# Variáveis
VENV_PATH = .venv
PYTHON = $(VENV_PATH)/bin/python
PIP = $(VENV_PATH)/bin/pip
PRE_COMMIT = $(VENV_PATH)/bin/pre-commit

# Exibe ajuda dos comandos
help:
	@echo ""
	@echo "📚 Comandos disponíveis:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

# Regra principal
all: install run test ## Instala dependências, executa o app e roda os testes

# Criação do ambiente virtual e instalação de dependências
install: ## Cria o ambiente virtual e instala as dependências
	@echo ""
	@echo "🔧 Verificando/criando ambiente virtual..."
	@if [ ! -d "$(VENV_PATH)" ]; then \
		python3 -m .venv $(VENV_PATH); \
	fi
	@echo "📦 Instalando dependências..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "✅ Dependências instaladas."

# Rodar a aplicação
run: ## Executa a aplicação principal
	@echo ""
	@echo "🚀 Executando app..."
	@if [ ! -f "app/main.py" ]; then \
		echo "❌ Erro: app/main.py não encontrado."; \
		exit 1; \
	fi
	@$(PYTHON) app/main.py
	@echo "✅ App finalizado."

# Rodar apenas testes unitários
test: ## Executa apenas os testes unitários
	@echo ""
	@echo "🧪 Executando testes..."
	@if [ ! -d "tests" ]; then \
		echo "❌ Erro: diretório tests/ não encontrado."; \
		exit 1; \
	fi
	@$(PYTHON) -m pytest tests/
	@echo "✅ Testes finalizados."

# Rodar testes + cobertura
coverage: ## Executa os testes e gera relatório de cobertura
	@echo ""
	@echo "🛡️  Executando testes com cobertura..."
	@if [ ! -d "tests" ]; then \
		echo "❌ Erro: diretório tests/ não encontrado."; \
		exit 1; \
	fi
	@$(PYTHON) -m pytest --cov=app --cov-report=html tests/
	@echo "✅ Testes e cobertura concluídos. Relatório em htmlcov/index.html."

# Rodar lint manualmente (pre-commit)
lint: ## Executa o pre-commit manualmente
	@echo ""
	@echo "🧹 Rodando pre-commit hooks..."
	@if [ ! -f "$(PRE_COMMIT)" ]; then \
		echo "❌ pre-commit não instalado. Execute 'make install' primeiro."; \
		exit 1; \
	fi
	@$(PRE_COMMIT) run --all-files
	@echo "✅ Pre-commit finalizado."

# Limpar ambiente
clean: ## Remove o ambiente virtual
	@echo ""
	@echo "🧹 Removendo ambiente virtual..."
	@rm -rf $(VENV_PATH)
	@echo "✅ Ambiente virtual removido."
