"""
Shared pytest fixtures.
"""

from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session

# Import all ORM models before creating sessions.
import src.models

from src.database.session import SessionLocal


@pytest.fixture
def session() -> Generator[Session, None, None]:
    """
    Create a database session for each test.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()