ifeq (, $(shell which poetry))
$(error "No poetry found in PATH, check out: https://github.com/python-poetry/poetry#installation")
endif

.PHONY: lint clean publish install check test

help:
	@echo "\n%% aiosnow dev tools %%"
	@echo - install: create venv and install dependencies
	@echo - update: update dependencies
	@echo - shell: activate virtual environment
	@echo - test: run tests
	@echo - publish: publish to pypi
	@echo - clean: remove cache and bytecode files
	@echo - lint: check code formatting
	@echo - reformat: reformat
	@echo ""

update:
	poetry update

install:
	poetry update

shell:
	poetry shell

test:
	poetry run python -m pytest

clean:
	rm -rf dist .mypy_cache docs/build .pytest_cache
	find aiosnow -type d -name __pycache__ -exec rm -rv {} +
	find aiosnow -type f -name "*.py[co]" -delete

publish:
	make clean
	poetry publish --build

lint:
	poetry run mypy aiosnow --disallow-untyped-defs
	poetry run autoflake --recursive aiosnow tests
	poetry run black aiosnow tests --check

reformat:
	poetry run autoflake --in-place --recursive aiosnow tests
	poetry run black aiosnow tests examples
	poetry run isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 aiosnow tests

