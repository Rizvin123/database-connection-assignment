from sqlalchemy import text

from src.database.session import SessionLocal


def test_database_connection():
    """Test that the application can connect to the MySQL database."""

    session = SessionLocal()

    try:
        result = session.execute(text("SELECT 1"))

        assert result.scalar() == 1

        print("✅ Successfully connected to the MySQL database.")

    finally:
        session.close()