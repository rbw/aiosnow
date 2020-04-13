ifeq (, $(shell which poetry))
$(error "No poetry found in PATH, check out: https://github.com/python-poetry/poetry#installation")
endif

.PHONY: lint clean publish install check test

help:
	@echo "\n%% Snow dev tools %%"
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
	poetry run python -m pytest --cov=snow --cov=tests --ignore venv

clean:
	rm -rf dist .mypy_cache
	find snow -type d -name __pycache__ -exec rm -rv {} +
	find snow -type f -name "*.py[co]" -delete

publish:
	make clean
	poetry publish --build

lint:
	poetry run mypy snow --disallow-untyped-defs
	poetry run autoflake --recursive snow tests
	poetry run black snow tests --check

reformat:
	poetry run autoflake --in-place --recursive snow tests
	poetry run black snow tests
	poetry run isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 --recursive --apply snow tests
