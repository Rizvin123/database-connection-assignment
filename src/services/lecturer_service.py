"""
Service layer for Lecturer operations.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.models.lecturer import Lecturer
from src.repositories.lecturer_repository import LecturerRepository


class LecturerService:
    """
    Service layer for Lecturer business logic.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        """
        Initialise the service.
        """

        self._repository = LecturerRepository(
            session,
        )

    def create_lecturer(
        self,
        lecturer: Lecturer,
    ) -> Lecturer:
        """
        Create a lecturer.
        """

        return self._repository.create(
            lecturer,
        )

    def get_lecturer(
        self,
        lecturer_id: int,
    ) -> Lecturer | None:
        """
        Retrieve a lecturer by ID.
        """

        return self._repository.get_by_id(
            lecturer_id,
        )

    def get_all_lecturers(
        self,
    ) -> list[Lecturer]:
        """
        Retrieve all lecturers.
        """

        return self._repository.get_all()

    def update_lecturer(
        self,
    ) -> None:
        """
        Persist pending lecturer changes.
        """

        self._repository.save()

    def delete_lecturer(
        self,
        lecturer_id: int,
    ) -> bool:
        """
        Delete a lecturer.
        """

        lecturer = self.get_lecturer(
            lecturer_id,
        )

        if lecturer is None:

            return False

        self._repository.delete(
            lecturer,
        )

        return True

    def find_by_email(
        self,
        email: str,
    ) -> Lecturer | None:
        """
        Find a lecturer by email.
        """

        return self._repository.find_by_email(
            email,
        )

    def find_by_department(
        self,
        department_id: int,
    ) -> list[Lecturer]:
        """
        Retrieve lecturers belonging to a department.
        """

        return self._repository.find_by_department(
            department_id,
        )

    def find_by_research_group(
        self,
        research_group_id: int,
    ) -> list[Lecturer]:
        """
        Retrieve lecturers belonging to a research group.
        """

        return self._repository.find_by_research_group(
            research_group_id,
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

        return self._repository.search_lecturers(
            search_field=search_field,
            search_text=search_text,
            department_id=department_id,
            research_group_id=research_group_id,
        )