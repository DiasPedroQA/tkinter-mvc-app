# Configurações básicas
SHELL := /bin/bash
VENV_PATH := .venv
PYTHON := $(VENV_PATH)/bin/python
PIP := $(VENV_PATH)/bin/pip
APP_PATH := app/main.py
LOG_DIR := .logs_makefile
LOG_FILE := $(LOG_DIR)/app.log

# Garante que o diretório de logs existe
$(shell mkdir -p $(LOG_DIR))

.PHONY: help install run test clean all limpar_log

# Função de log com timestamp
define log
	echo "[$$(date '+%Y-%m-%d %H:%M:%S')] $(1)" | tee -a $(LOG_FILE)
endef

# Ajuda
help: ## Mostra todos os comandos disponíveis
	@$(call log,"📚 Comandos disponíveis:")
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' | tee -a $(LOG_FILE)

# Regra principal
all: limpar_log install run test ## Executa tudo: instalação, aplicação e testes

# Limpa o log antes de executar qualquer coisa
limpar_log:
	@echo "" > $(LOG_FILE)
	@$(call log,"🧼 Log limpo para nova execução.")

# Instalação
install: ## Cria ambiente virtual e instala dependências
	@$(call log,"🔧 Verificando ambiente virtual...")
	@if [ ! -d "$(VENV_PATH)" ]; then \
		echo "Criando novo ambiente virtual..." | tee -a $(LOG_FILE); \
		python3 -m venv "$(VENV_PATH)" || { echo "❌ Falha ao criar ambiente virtual" | tee -a $(LOG_FILE); exit 1; }; \
	fi

	@$(call log,"📦 Atualizando pip e wheel...")
	@$(PIP) install --upgrade pip wheel >> $(LOG_FILE) 2>&1 || { echo "❌ Falha ao atualizar pip/wheel" | tee -a $(LOG_FILE); exit 1; }

	@$(call log,"🔍 Procurando arquivos de dependências...")
	@if [ -f "pyproject.toml" ]; then \
		$(call log,"📦 Instalando projeto em modo editável..."); \
		$(PIP) install -e . >> $(LOG_FILE) 2>&1 || { echo "❌ Falha na instalação editável" | tee -a $(LOG_FILE); exit 1; }; \
	elif [ -f "requirements.txt" ]; then \
		$(call log,"📦 Instalando de requirements.txt..."); \
		$(PIP) install -r requirements.txt >> $(LOG_FILE) 2>&1 || { echo "❌ Falha na instalação de requirements.txt" | tee -a $(LOG_FILE); exit 1; }; \
	else \
		$(call log,"⚠ Aviso: Nenhum arquivo de dependências encontrado."); \
	fi
	@$(call log,"✅ Instalação concluída.")

# Execução da aplicação
run: ## Executa a aplicação principal
	@$(call log,"🚀 Iniciando aplicação...")
	@if [ ! -f "$(APP_PATH)" ]; then \
		echo "❌ Erro: Arquivo principal não encontrado em $(APP_PATH)" | tee -a $(LOG_FILE); \
		exit 1; \
	fi
	@$(PYTHON) $(APP_PATH) >> $(LOG_FILE) 2>&1 || { echo "❌ Aplicação falhou" | tee -a $(LOG_FILE); exit 1; }
	@$(call log,"✅ Aplicação finalizada.")

# Testes
test: ## Executa os testes
	@$(call log,"🧪 Rodando testes...")
	@$(PYTHON) -m pytest -v >> $(LOG_FILE) 2>&1 || { echo "❌ Testes falharam" | tee -a $(LOG_FILE); exit 1; }
	@$(call log,"✅ Testes concluídos com sucesso!")
	@$(MAKE) run

# Limpeza
clean: ## Remove o ambiente virtual e arquivos temporários
	@$(call log,"🧹 Limpando ambiente...")
	@rm -rf "$(VENV_PATH)" >> $(LOG_FILE) 2>&1
	@find . -type d -name "__pycache__" -exec rm -rf {} + >> $(LOG_FILE) 2>&1
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + >> $(LOG_FILE) 2>&1
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + >> $(LOG_FILE) 2>&1
	@$(call log,"✅ Limpeza concluída.")
