.PHONY: install test run clean all

install:
	@echo "Instalando dependências..."
	. .venv/bin/activate && pip install -r requirements.txt

test:
	@echo "Executando testes..."
	. .venv/bin/activate && pytest -v

run:
	@echo "Iniciando a aplicação..."
	. .venv/bin/activate && python src/app.py

all: install test run

clean:
	@echo "Removendo arquivos temporários..."
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf .coverage
