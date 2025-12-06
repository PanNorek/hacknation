from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

from .base import Base


class CountryData(Base):
    """SQLAlchemy model for country_data table."""

    __tablename__ = "country_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_name = Column(Text, nullable=False)
    geographical_features = Column(Text, nullable=True)
    population = Column(Text, nullable=True)
    climate = Column(Text, nullable=True)
    economic_strengths = Column(Text, nullable=True)
    army_size = Column(Text, nullable=True)
    digitalization_level = Column(Text, nullable=True)
    currency = Column(Text, nullable=True)
    key_bilateral_relations = Column(JSONB, nullable=True)
    political_economic_threats = Column(Text, nullable=True)
    military_threats = Column(Text, nullable=True)
    development_milestones = Column(Text, nullable=True)
    embedding = Column(Vector(384), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=True
    )

    def __repr__(self):
        return f"<CountryData(id={self.id}, country_name='{self.country_name}')>"
