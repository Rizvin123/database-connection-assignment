"""
Common mixins shared across SQLAlchemy models.
"""

from sqlalchemy.inspection import inspect


class ReprMixin:
    """
    Provides a readable string representation for SQLAlchemy models.
    """

    def __repr__(self) -> str:
        values = []

        for column in inspect(self).mapper.column_attrs:
            value = getattr(self, column.key)
            values.append(f"{column.key}={value!r}")

        return (
            f"{self.__class__.__name__}"
            f"({', '.join(values)})"
        )