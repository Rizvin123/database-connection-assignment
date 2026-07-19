"""
Generic SQLAlchemy repository.
"""

from __future__ import annotations

from typing import Generic
from typing import Type
from typing import TypeVar

from sqlalchemy.orm import Session

from src.database.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """
    Generic repository providing CRUD operations for SQLAlchemy models.
    """

    def __init__(
        self,
        session: Session,
        model: Type[T],
    ) -> None:
        """
        Initialise the repository.

        Parameters
        ----------
        session:
            SQLAlchemy database session.

        model:
            ORM model managed by this repository.
        """

        self._session = session
        self._model = model

    def create(
        self,
        entity: T,
    ) -> T:
        """
        Insert a new entity into the database.
        """

        self._session.add(entity)
        self._session.commit()
        self._session.refresh(entity)

        return entity

    def get_by_id(
        self,
        entity_id,
    ) -> T | None:
        """
        Retrieve an entity by its primary key.
        """

        return self._session.get(
            self._model,
            entity_id,
        )

    def get_all(
        self,
    ) -> list[T]:
        """
        Retrieve every row.
        """

        return (
            self._session
            .query(self._model)
            .all()
        )

    def save(
        self,
    ) -> None:
        """
        Commit pending changes.
        """

        self._session.commit()

        self._session.expire_all()

    def delete(
        self,
        entity: T,
    ) -> None:
        """
        Delete an entity.
        """

        self._session.delete(entity)
        self._session.commit()