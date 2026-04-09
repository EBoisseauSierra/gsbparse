.PHONY: default install test lint format type-check import-check ci

default:
	@echo "Targets: install test lint format type-check import-check ci"

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

ci: lint format type-check import-check test
