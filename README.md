# HackNation AI Agent API

A FastAPI application that provides access to a Gemini AI agent for querying country information about Atlantis.

## Features

- **Gemini AI Agent**: Powered by Google's Gemini models
- **Country Data**: Pre-loaded with comprehensive Atlantis country information
- **Vector Database**: PostgreSQL with pgvector for similarity search
- **RESTful API**: Clean endpoints for agent interaction
- **Structured Logging**: Comprehensive logging configuration with startup/shutdown events
- **Pydantic Models**: Type-safe request/response handling
- **Configurable**: Extensive configuration via environment variables

## Database Setup

The project uses PostgreSQL with pgvector extension for vector similarity search.

### Using Docker Compose (Recommended)

```bash
# Start PostgreSQL with pgvector
docker-compose up -d

# Check if database is ready
docker-compose logs postgres

# Run database tests
python src/db/test.py
```

### Manual Docker Build

```bash
# Build PostgreSQL container with pgvector and auto-migrations
docker build -f src/db/Dockerfile -t hacknation-postgres .

# Run container (migrations run automatically during database initialization)
docker run -d \
  --name hacknation-postgres \
  -p 5432:5432 \
  -e POSTGRES_DB=hacknation \
  -e POSTGRES_USER=hacknation_user \
  -e POSTGRES_PASSWORD=hacknation_password \
  hacknation-postgres

# Check logs to see migration progress (runs during first startup)
docker logs hacknation-postgres

# Container runs PostgreSQL normally after migrations complete
```

### Database Configuration

Create a `.env` file with database settings:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hacknation
DB_USER=hacknation_user
DB_PASSWORD=hacknation_password

# ... other settings ...
```

### Database Schema & Models

The database includes three main tables with vector columns and corresponding SQLAlchemy models:

#### Tables & Models
- **`embeddings`** → `Embedding` model: General text embeddings (384-dim vectors)
- **`instructions`** → `Instruction` model: User instructions with embeddings
- **`country_data`** → `CountryData` model: Atlantis country information with embeddings

#### Features
- **Vector similarity search** enabled with IVFFlat indexes for fast queries
- **JSONB metadata** storage for flexible data
- **Automatic timestamps** with timezone support
- **Cosine similarity functions** for vector operations

#### Usage Examples

```python
from src.db import EmbeddingRepository, create_embedding, find_similar_embeddings

# Create and store an embedding
embedding = create_embedding(
    content="Example text",
    embedding=[0.1, 0.2, ...],  # 384-dim vector
    metadata={"source": "example"}
)

# Find similar content
similar = find_similar_embeddings(query_embedding, limit=5, threshold=0.8)

# Work with Atlantis data
atlantis = get_atlantis_data()
print(f"Population: {atlantis.population}")
```

### Database Migrations with Alembic

The project includes Alembic for database schema migrations:

```bash
# Initialize database (if not already done)
make db-init

# Create a new migration
make db-migrate msg="add new table"

# Apply migrations
make db-upgrade

# View migration history
make db-history

# Check current migration status
make db-current
```

### Alembic Commands

```bash
# Create new migration file
alembic revision -m "description"

# Auto-generate migration from model changes
alembic revision --autogenerate -m "auto update"

# Apply all migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration status
alembic current
```

## Quick Start

```bash
# Install dependencies
uv sync

# Start database
docker-compose up -d

# Run the API
make run-api
# or
uv run uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000 with automatic logging of all requests and application events.

## API Endpoints

### GET /
Basic API information and available endpoints.

### POST /prompt
Send prompts to the Gemini AI agent.

**Request Body**:
```json
{
  "prompt": "What is the population of Atlantis?",
  "context": {"additional": "data"}
}
```

### GET /agent_info
Get information about the Gemini AI agent.

### POST /instructions
Save user instructions.

**Request Body**:
```json
{
  "instructions": "Custom instructions for the AI agent"
}
```

### GET /country_data
Get the Atlantis country data used by the agent.

## Testing

You can test the API using curl:

```bash
# Test the root endpoint
curl http://localhost:8000/

# Test agent info
curl http://localhost:8000/agent_info

# Test prompting
curl -X POST http://localhost:8000/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Atlantis known for economically?"}'
```

Or use the interactive API documentation at: http://localhost:8000/docs

## Database Testing

Run the database tests to verify vector operations:

```bash
# Test database connection and vector operations
python src/db/test.py
```

This will test:
- Database connectivity
- Vector operations
- Embedding storage and retrieval
- Similarity search functionality
