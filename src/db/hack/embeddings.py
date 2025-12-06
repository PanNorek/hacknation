from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

from .base import Base


class Embedding(Base):
    """SQLAlchemy model for embeddings table."""

    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384), nullable=True)
    metadata = Column(JSONB, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=True
    )

    def __repr__(self):
        return f"<Embedding(id={self.id}, content='{self.content[:50]}...', embedding={self.embedding is not None})>"
