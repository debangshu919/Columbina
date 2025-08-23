.PHONY: run lint format docker-build docker-up docker-down

lint:
	flake8 src

format:
	black src
	isort src

run:
	uv run src/main.py
	
docker-build:
	docker build -t columbina .
	
docker-up:
	docker-compose up --build -d
	
docker-down:
	docker-compose down