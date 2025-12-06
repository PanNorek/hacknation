run:
	uv run main.py
format:
	uvx black . --line-length 88
lint:
	uvx flake8 .
run-api:
	uv run uvicorn src.api:app --reload --host 0.0.0.0 --port 8000 --log-level info
