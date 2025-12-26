
.PHONY: install format precommit publish build clean


.venv:
	uv venv

format:
	uvx black .
	uvx isort .

precommit: format

build: .venv format precommit
	uv build

publish: build
	uv publish

clean:
	rm -rf .venv/
