install:
    pip install -r requirements.txt

test:
    python -m unittest discover tests

run:
    python src/app.py
