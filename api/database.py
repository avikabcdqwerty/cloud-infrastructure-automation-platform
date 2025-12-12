import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load database URL from environment variable for security and flexibility
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/cloud_infra_db"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False,  # Set to True for SQL debugging
    future=True
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Exports:
# - engine: SQLAlchemy engine instance
# - SessionLocal: session factory for DB sessions