"""
Verify that all SQLAlchemy ORM models can be configured successfully.
"""

from sqlalchemy.orm import configure_mappers


def test_model_configuration() -> None:
    """
    Ensure all ORM relationships are configured without errors.
    """
    configure_mappers()