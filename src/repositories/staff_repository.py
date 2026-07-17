"""
Repository for Staff database operations.
"""

from __future__ import annotations

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.models.staff import Staff
from src.repositories.base_repository import BaseRepository


class StaffRepository(BaseRepository[Staff]):
    """
    Repository for Staff entities.
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
            Staff,
        )

    def find_by_email(
        self,
        email: str,
    ) -> Staff | None:
        """
        Retrieve a staff member by email.
        """

        return (
            self._session.query(Staff)
            .filter(
                Staff.email == email,
            )
            .first()
        )

    def find_by_department(
        self,
        department_id: int,
    ) -> list[Staff]:
        """
        Retrieve staff in a department.
        """

        return (
            self._session.query(Staff)
            .filter(
                Staff.department_id == department_id,
            )
            .order_by(
                Staff.last_name,
                Staff.first_name,
            )
            .all()
        )

    def find_by_job_title(
        self,
        job_title: str,
    ) -> list[Staff]:
        """
        Retrieve staff by job title.
        """

        return (
            self._session.query(Staff)
            .filter(
                Staff.job_title == job_title,
            )
            .order_by(
                Staff.last_name,
                Staff.first_name,
            )
            .all()
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

        query = self._session.query(Staff)

        if search_text:

            search_text = search_text.strip()

            if search_field == "first_name":

                query = query.filter(
                    Staff.first_name.ilike(
                        f"%{search_text}%"
                    )
                )

            elif search_field == "last_name":

                query = query.filter(
                    Staff.last_name.ilike(
                        f"%{search_text}%"
                    )
                )

            elif search_field == "email":

                query = query.filter(
                    Staff.email.ilike(
                        f"%{search_text}%"
                    )
                )

            else:

                query = query.filter(
                    or_(
                        Staff.first_name.ilike(
                            f"%{search_text}%"
                        ),
                        Staff.last_name.ilike(
                            f"%{search_text}%"
                        ),
                        Staff.email.ilike(
                            f"%{search_text}%"
                        ),
                    )
                )

        if department_id is not None:

            query = query.filter(
                Staff.department_id == department_id,
            )

        if job_title:

            query = query.filter(
                Staff.job_title == job_title,
            )

        return (
            query.order_by(
                Staff.last_name,
                Staff.first_name,
            )
            .all()
        )

    def exists(
        self,
        email: str,
    ) -> bool:
        """
        Determine whether a staff member with the supplied email exists.
        """

        return self.find_by_email(email) is not None