"""
Repository for Lecturer ORM operations.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.models.lecturer import Lecturer
from src.repositories.base_repository import BaseRepository


class LecturerRepository(BaseRepository[Lecturer]):
    """
    Repository providing Lecturer-specific database operations.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=Lecturer,
        )

    def get_advisors(
        self,
    ) -> list[Lecturer]:
        """
        Retrieve lecturers ordered by surname then first name.
        """

        return (
            self._session.query(Lecturer)
            .order_by(
                Lecturer.last_name,
                Lecturer.first_name,
            )
            .all()
        )