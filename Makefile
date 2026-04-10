.PHONY: default install test lint format type-check import-check docs doctest ci

default:
	@echo "Targets: install test lint format type-check import-check docs doctest ci"

install:
	uv sync --dev

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

type-check:
	uv run mypy

import-check:
	uv run lint-imports

docs:
	uv run sphinx-build -b html docs docs/_build/html

doctest:
	uv run sphinx-build -b doctest docs docs/_build/doctest

ci: lint format type-check import-check test doctest
