install:
	pip install -r requirements.txt

run:
	python app/main.py

test:
	pytest tests/
