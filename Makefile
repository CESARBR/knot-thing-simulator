PYTHONPATH := .
VENV := venv
BIN := $(VENV)/bin

PYTHON := env PYTHONPATH=$(PYTHONPATH) $(BIN)/python
PIP := $(BIN)/pip
PYTEST := $(BIN)/pytest

REQUIREMENTS := -r requirements.txt
PRE_COMMIT := $(BIN)/pre-commit

PYMODULE := simulator
PYAPP := knot_thing_simulator

TESTS := tests
run:
	sudo $(PYTHON) $(PYAPP).py

bootstrap: venv \
	   requirements \
	   pre-commit-hooks

venv:
	python3 -m venv $(VENV)

requirements:
	$(PIP) install $(REQUIREMENTS)

pre-commit-hooks:
	cp hooks/pre-commit .git/hooks/pre-commit
	$(PRE_COMMIT) install

clean:
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

clean-all: clean
		rm -r $(VENV)
		rm .git/hooks/pre-commit

test:
	$(PYTEST) --cov=$(PYMODULE) $(TESTS)
