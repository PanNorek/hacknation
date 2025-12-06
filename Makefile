run:
	uv run main.py
format:
	uvx black . --line-length 88
lint:
	uvx flake8 .
