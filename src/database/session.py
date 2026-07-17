"""
Creates and manages the SQLAlchemy database engine and session factory.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.config import DATABASE_URL


# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False,          # Set to True if you want to see SQL statements
    pool_pre_ping=True   # Checks connections before using them
)

# Create a session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)