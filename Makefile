run:
	uv run main.py
format:
	uvx black . --line-length 88
lint:
	uvx flake8 .
run-api:
	uv run uvicorn src.api:app --reload --host 0.0.0.0 --port 8000 --log-level info
db-up:
	docker build -f src/db/Dockerfile -t hacknation-db . && docker run -d --name hacknation-db -p 5455:5432 -e POSTGRES_DB=hack -e POSTGRES_USER=hack -e POSTGRES_PASSWORD=hack hacknation-db
migrate:
	uv run alembic upgrade head

embeddings:
	uv run python scripts/embedding_job.py
