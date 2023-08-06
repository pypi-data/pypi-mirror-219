SHELL = /bin/bash
DESTDIR ?= /
SOURCES := $(shell find arch_release_promotion -name '*.py' -or -type d) arch_release_promotion pyproject.toml

all: build

fmt:
	black .
	isort .

coverage:
	python -X dev -m coverage run
	coverage xml
	coverage html
	coverage report --fail-under=100.0

lint:
	isort --check .
	black --check .
	pydocstyle .
	flake8
	bandit -c pyproject.toml -r .
	mypy --install-types --non-interactive -p arch_release_promotion -p tests
	vulture arch_release_promotion tests

build: $(SOURCES)
	python -m build --wheel --no-isolation

integration:
	pytest -m 'integration'

test:
	pytest -vv -k 'not integration'

install:
	python -m installer --destdir="$(DESTDIR)" dist/*.whl

clean:
	rm -rf dist

.PHONY: all lint fmt test build clean install regex
