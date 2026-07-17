"""
Repository for Department operations.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.models.department import Department
from src.repositories.base_repository import BaseRepository


class DepartmentRepository(BaseRepository[Department]):
    """
    Repository for Department entities.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        """
        Initialise the repository.
        """

        super().__init__(
            session,
            Department,
        )

    def get_department_names(
        self,
    ) -> list[Department]:
        """
        Retrieve all departments ordered by name.
        """

        return (
            self._session.query(Department)
            .order_by(
                Department.department_name,
            )
            .all()
        )