SHELL = /bin/bash
DESTDIR ?= /
SOURCES := $(shell find repod -name '*.py' -or -type d) repod pyproject.toml

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
	mypy --install-types --non-interactive -p repod -p tests
	vulture --min-confidence 70 repod tests

docs:
	repod-file schema export docs/schema/
	PYTHONPATH="$(PWD)" sphinx-build -M html docs/ docs/_build/
	PYTHONPATH="$(PWD)" sphinx-build -b man docs/ docs/_build/man/

system-docs:
	python -c 'from repod import export_schemas; from pathlib import Path; export_schemas(Path("docs/schema/"))'
	PYTHONPATH="$(PWD)" sphinx-build -M html docs/ docs/_build/
	PYTHONPATH="$(PWD)" sphinx-build -b man docs/ docs/_build/man/

build: $(SOURCES)
	python -m build --wheel --no-isolation

regex:
	pytest -m "regex"

integration:
	pytest -m "integration"

test:
	pytest -vv -k 'not (integration or regex)'

install:
	python -m installer --destdir="$(DESTDIR)" dist/*.whl
	install -vDm 644 docs/_build/man/man1/*.1 -t "$(DESTDIR)/usr/share/man/man1/"
	install -vDm 644 docs/_build/man/man5/*.5 -t "$(DESTDIR)/usr/share/man/man5/"
	install -vdm 755 "$(DESTDIR)/etc/repod.conf.d/"
	install -vdm 755 "$(DESTDIR)/var/lib/repod/management/"
	install -vdm 755 "$(DESTDIR)/var/lib/repod/data/pool/package/"
	install -vdm 755 "$(DESTDIR)/var/lib/repod/data/pool/source/"
	install -vdm 755 "$(DESTDIR)/var/lib/repod/data/repo/package/"
	install -vdm 755 "$(DESTDIR)/var/lib/repod/data/repo/source/"

clean:
	rm -rf dist build docs/_build

.PHONY: all build clean coverage docs fmt install lint regex system-docs test
