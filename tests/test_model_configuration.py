"""
Verify that all SQLAlchemy ORM models can be configured successfully.
"""

import src.models

from sqlalchemy.orm import configure_mappers


def test_model_configuration() -> None:
    """
    Ensure every SQLAlchemy mapper can be configured.
    """
    configure_mappers()