"""
Service layer for Staff operations.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.models.staff import Staff
from src.repositories.staff_repository import StaffRepository


class StaffService:
    """
    Service layer for Staff business logic.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        """
        Initialise the service.
        """

        self._repository = StaffRepository(
            session,
        )

    def create_staff(
        self,
        staff: Staff,
    ) -> Staff:
        """
        Create a staff member.
        """

        return self._repository.create(
            staff,
        )

    def get_staff(
        self,
        staff_id: int,
    ) -> Staff | None:
        """
        Retrieve a staff member by ID.
        """

        return self._repository.get_by_id(
            staff_id,
        )

    def get_all_staff(
        self,
    ) -> list[Staff]:
        """
        Retrieve all staff.
        """

        return self._repository.get_all()

    def update_staff(
        self,
    ) -> None:
        """
        Persist pending staff changes.
        """

        self._repository.save()

    def delete_staff(
        self,
        staff_id: int,
    ) -> bool:
        """
        Delete a staff member.
        """

        staff = self.get_staff(
            staff_id,
        )

        if staff is None:

            return False

        self._repository.delete(
            staff,
        )

        return True

    def find_by_email(
        self,
        email: str,
    ) -> Staff | None:
        """
        Find a staff member by email.
        """

        return self._repository.find_by_email(
            email,
        )

    def find_by_department(
        self,
        department_id: int,
    ) -> list[Staff]:
        """
        Retrieve staff in a department.
        """

        return self._repository.find_by_department(
            department_id,
        )

    def find_by_job_title(
        self,
        job_title: str,
    ) -> list[Staff]:
        """
        Retrieve staff by job title.
        """

        return self._repository.find_by_job_title(
            job_title,
        )

    def search_staff(
        self,
        *,
        search_field: str | None = None,
        search_text: str | None = None,
        department_id: int | None = None,
        job_title: str | None = None,
    ) -> list[Staff]:
        """
        Search staff using optional filters.
        """

        return self._repository.search_staff(
            search_field=search_field,
            search_text=search_text,
            department_id=department_id,
            job_title=job_title,
        )

    def staff_exists(
        self,
        email: str,
    ) -> bool:
        """
        Determine whether a staff member exists.
        """

        return self._repository.exists(
            email,
        )