.PHONY: run test lint format docker-build docker-up docker-down

lint:
	flake8 src tests

format:
	black src tests
	isort src tests

run:
	uv run main.py
	
test:
	pytest -v
	
docker-build:
	docker build -t columbina .
	
docker-up:
	docker-compose up --build -d
	
docker-down:
	docker-compose down