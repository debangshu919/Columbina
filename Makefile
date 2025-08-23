.PHONY: run test lint format docker-build docker-up

lint:
	flake8 src tests

format:
	black src tests
	isort src tests

run:
	uv run main.py