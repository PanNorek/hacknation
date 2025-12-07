from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from pgvector.sqlalchemy import Vector

from .base import Base


class Instruction(Base):
    """SQLAlchemy model for instructions table."""

    __tablename__ = "instructions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    instructions = Column(Text, nullable=False)
    embedding = Column(Vector(384), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=True
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    def __repr__(self):
        return (
            f"<Instruction(id={self.id}, instructions='{self.instructions[:50]}...')>"
        )
