"""Initial migration

Revision ID: 001
Revises:
Create Date: 2024-12-06 19:45:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema."""

    # Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Create embeddings table
    op.create_table(
        "embeddings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(384), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create index for embeddings
    op.create_index(
        "embeddings_embedding_idx",
        "embeddings",
        ["embedding"],
        postgresql_using="ivfflat",
        postgresql_ops={"embedding": "vector_cosine_ops"},
    )

    # Create instructions table
    op.create_table(
        "instructions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("instructions", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(384), nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create index for instructions
    op.create_index(
        "instructions_embedding_idx",
        "instructions",
        ["embedding"],
        postgresql_using="ivfflat",
        postgresql_ops={"embedding": "vector_cosine_ops"},
    )

    # Create country_data table
    op.create_table(
        "country_data",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("country_name", sa.String(length=255), nullable=False),
        sa.Column("geographical_features", sa.Text(), nullable=True),
        sa.Column("population", sa.String(length=100), nullable=True),
        sa.Column("climate", sa.String(length=100), nullable=True),
        sa.Column("economic_strengths", sa.Text(), nullable=True),
        sa.Column("army_size", sa.String(length=100), nullable=True),
        sa.Column("digitalization_level", sa.String(length=255), nullable=True),
        sa.Column("currency", sa.String(length=100), nullable=True),
        sa.Column("key_bilateral_relations", postgresql.JSONB(), nullable=True),
        sa.Column("political_economic_threats", sa.Text(), nullable=True),
        sa.Column("military_threats", sa.Text(), nullable=True),
        sa.Column("development_milestones", sa.Text(), nullable=True),
        sa.Column("embedding", Vector(384), nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create index for country_data
    op.create_index(
        "country_data_embedding_idx",
        "country_data",
        ["embedding"],
        postgresql_using="ivfflat",
        postgresql_ops={"embedding": "vector_cosine_ops"},
    )

    # Create cosine_similarity function
    op.execute(
        """
        CREATE OR REPLACE FUNCTION cosine_similarity(a vector, b vector)
        RETURNS float
        LANGUAGE sql IMMUTABLE STRICT PARALLEL SAFE
        AS $$
            SELECT 1 - (a <=> b)
        $$;
    """
    )

    # Create find_similar_embeddings function
    op.execute(
        """
        CREATE OR REPLACE FUNCTION find_similar_embeddings(query_embedding vector, match_threshold float DEFAULT 0.7, match_count int DEFAULT 10)
        RETURNS TABLE(id int, content text, similarity float)
        LANGUAGE sql STABLE STRICT PARALLEL SAFE
        AS $$
            SELECT
                e.id,
                e.content,
                cosine_similarity(e.embedding, query_embedding) as similarity
            FROM embeddings e
            WHERE cosine_similarity(e.embedding, query_embedding) > match_threshold
            ORDER BY cosine_similarity(e.embedding, query_embedding) DESC
            LIMIT match_count;
        $$;
    """
    )

    # Insert default Atlantis data
    op.execute(
        """
        INSERT INTO country_data (
            country_name,
            geographical_features,
            population,
            climate,
            economic_strengths,
            army_size,
            digitalization_level,
            currency,
            key_bilateral_relations,
            political_economic_threats,
            military_threats,
            development_milestones
        ) VALUES (
            'Atlantis',
            'access to the Baltic Sea, several large navigable rivers, limited drinking water resources',
            '28 million',
            'temperate',
            'heavy industry, automotive, food, chemical, ICT, ambitions to play a significant role in renewable energy sources, processing critical raw materials and building supranational AI infrastructure (including big data centers, AI giga factories, quantum computers)',
            '150 thousand professional soldiers',
            'above European average',
            'other than euro',
            '["Germany", "France", "Finland", "Ukraine", "USA", "Japan"]'::jsonb,
            'instability in the EU, disintegration of the EU into "different speeds" groups in terms of development pace and interest in deeper integration; negative image campaign by several state actors aimed against the Atlantis government or society; disruptions in hydrocarbon fuel supplies from the USA, Scandinavia, Persian Gulf (resulting from potential changes in the internal policies of exporting countries or transport problems, e.g. Houthi attacks on tankers in the Red Sea); exposure to slowdown in ICT sector development due to embargo on advanced processors',
            'threat of armed attack by one of the neighbors; ongoing hybrid attacks by at least one neighbor for many years, including in the area of critical infrastructure and cyberspace',
            'parliamentary democracy for 130 years; periods of economic stagnation in 1930-1950 and 1980-1990; EU and NATO membership since 1997; 25th largest economy in the world by GDP since 2020; budget deficit and public debt around EU average'
        );
    """
    )


def downgrade() -> None:
    """Downgrade database schema."""

    # Drop functions
    op.execute("DROP FUNCTION IF EXISTS find_similar_embeddings(vector, float, int)")
    op.execute("DROP FUNCTION IF EXISTS cosine_similarity(vector, vector)")

    # Drop indexes
    op.drop_index("country_data_embedding_idx", table_name="country_data")
    op.drop_index("instructions_embedding_idx", table_name="instructions")
    op.drop_index("embeddings_embedding_idx", table_name="embeddings")

    # Drop tables
    op.drop_table("country_data")
    op.drop_table("instructions")
    op.drop_table("embeddings")

    # Drop extension (optional - usually kept)
    # op.execute("DROP EXTENSION IF EXISTS vector")
