def load_system_prompt(file_path: str) -> str:
    """Load the system prompt for AI agent from a specified file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileExistsError("Error: System prompt file not found.") from e
