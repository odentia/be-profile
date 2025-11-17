.PHONY: help install migrate run test clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make migrate    - Run database migrations"
	@echo "  make run        - Run the service"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean cache files"

install:
	uv sync

migrate:
	uv run alembic upgrade head

run:
	uv run python -m profile_service.api

test:
	uv run pytest

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

