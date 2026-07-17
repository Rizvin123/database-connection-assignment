"""
Repository for Lecturer operations.
"""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.lecturer import Lecturer
from src.repositories.base_repository import BaseRepository


class LecturerRepository(BaseRepository[Lecturer]):
    """
    Repository for Lecturer entities.
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
            Lecturer,
        )

    def find_by_email(
        self,
        email: str,
    ) -> Lecturer | None:
        """
        Find a lecturer by email.
        """

        return (
            self._session.query(Lecturer)
            .filter(
                func.lower(Lecturer.email)
                == email.lower()
            )
            .first()
        )

    def find_by_department(
        self,
        department_id: int,
    ) -> list[Lecturer]:
        """
        Retrieve lecturers belonging to a department.
        """

        return (
            self._session.query(Lecturer)
            .filter(
                Lecturer.department_id == department_id
            )
            .order_by(
                Lecturer.last_name,
                Lecturer.first_name,
            )
            .all()
        )

    def find_by_research_group(
        self,
        research_group_id: int,
    ) -> list[Lecturer]:
        """
        Retrieve lecturers belonging to a research group.
        """

        return (
            self._session.query(Lecturer)
            .filter(
                Lecturer.research_group_id
                == research_group_id
            )
            .order_by(
                Lecturer.last_name,
                Lecturer.first_name,
            )
            .all()
        )

    def search_lecturers(
        self,
        *,
        search_field: str | None = None,
        search_text: str | None = None,
        department_id: int | None = None,
        research_group_id: int | None = None,
    ) -> list[Lecturer]:
        """
        Search lecturers using optional filters.
        """

        query = self._session.query(Lecturer)

        if search_text:

            value = f"%{search_text}%"

            if search_field == "first_name":

                query = query.filter(
                    Lecturer.first_name.ilike(value)
                )

            elif search_field == "last_name":

                query = query.filter(
                    Lecturer.last_name.ilike(value)
                )

            elif search_field == "email":

                query = query.filter(
                    Lecturer.email.ilike(value)
                )

        if department_id is not None:

            query = query.filter(
                Lecturer.department_id == department_id
            )

        if research_group_id is not None:

            query = query.filter(
                Lecturer.research_group_id
                == research_group_id
            )

        return (
            query.order_by(
                Lecturer.last_name,
                Lecturer.first_name,
            )
            .all()
        )

    def get_advisors(
        self,
    ) -> list[Lecturer]:
        """
        Retrieve lecturers for advisor selection.
        """

        return (
            self._session.query(Lecturer)
            .order_by(
                Lecturer.last_name,
                Lecturer.first_name,
            )
            .all()
        )