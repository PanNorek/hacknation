# Development commands (run locally)
run:
	uv run main.py

format:
	uvx black . --line-length 88

lint:
	uvx flake8 .

# Docker Compose commands (run full stack)
up:
	docker-compose up --build

up-d:
	docker-compose up --build -d

down:
	docker-compose down

down-v:
	docker-compose down -v

# Individual service commands with docker-compose
run-api:
	docker-compose up --build app

db-up:
	docker-compose up --build postgres -d

migrate:
	docker-compose exec app uv run alembic upgrade head

create-embeddings:
	docker-compose exec app uv run python create_embeddings.py

# Logs and debugging
logs:
	docker-compose logs -f

logs-app:
	docker-compose logs -f app

logs-db:
	docker-compose logs -f postgres

# Database management
db-shell:
	docker-compose exec postgres psql -U postgres -d hacknation

# Cleanup
clean:
	docker-compose down -v --rmi all
	docker system prune -f

.PHONY: run format lint up up-d down down-v run-api db-up migrate create-embeddings logs logs-app logs-db db-shell clean