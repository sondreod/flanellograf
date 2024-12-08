VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

.PHONY: install format precommit publish build clean


venv:
	python3 -m venv $(VENV_DIR)
	$(PIP) install -e .[dev]

dev: venv
	@cat $(VENV_DIR)/bin/activate > dev
	@echo export PYTHONPATH=$(PWD)/ >> dev
	@echo "Dev environment ready, type '. dev' to activate"

format:
	black .
	isort .

precommit: format

build: precommit
	flit build

publish: build
	flit publish

clean:
	rm -rf venv/
	rm dev
