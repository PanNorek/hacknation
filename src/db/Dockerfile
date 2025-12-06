# Use PostgreSQL 15 as base image
FROM postgres:15

# Install build dependencies for pgvector and Python tools
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-15 \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install Alembic, SQLAlchemy, and pgvector for migrations
RUN pip3 install --break-system-packages alembic sqlalchemy psycopg2-binary pgvector

# Clone and build pgvector
RUN cd /tmp \
    && git clone --branch v0.7.0 https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install

# Copy Alembic configuration and migrations
COPY alembic.ini /alembic.ini
COPY ./migrations /migrations


# Expose PostgreSQL port
EXPOSE 5432

# Use standard PostgreSQL CMD (migrations run automatically during init)
CMD ["postgres"]


