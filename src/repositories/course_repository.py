"""
Repository for Course operations.
"""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.course import Course
from src.repositories.base_repository import BaseRepository


class CourseRepository(BaseRepository[Course]):
    """
    Repository for Course entities.
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
            Course,
        )

    def find_by_course_name(
        self,
        course_name: str,
    ) -> list[Course]:
        """
        Retrieve courses matching a course name.
        """

        return (
            self._session.query(Course)
            .filter(
                Course.course_name.ilike(
                    f"%{course_name}%"
                )
            )
            .order_by(
                Course.course_name,
            )
            .all()
        )

    def find_by_department(
        self,
        department_id: int,
    ) -> list[Course]:
        """
        Retrieve courses belonging to a department.
        """

        return (
            self._session.query(Course)
            .filter(
                Course.department_id == department_id
            )
            .order_by(
                Course.course_name,
            )
            .all()
        )

    def find_by_level(
        self,
        level: int,
    ) -> list[Course]:
        """
        Retrieve courses at a particular level.
        """

        return (
            self._session.query(Course)
            .filter(
                Course.level == level
            )
            .order_by(
                Course.course_name,
            )
            .all()
        )

    def search_courses(
        self,
        *,
        search_field: str | None = None,
        search_text: str | None = None,
        department_id: int | None = None,
        level: int | None = None,
    ) -> list[Course]:
        """
        Search courses using optional filters.
        """

        query = self._session.query(
            Course,
        )

        if search_text:

            value = f"%{search_text}%"

            if search_field == "course_code":

                query = query.filter(
                    Course.course_code.ilike(
                        value
                    )
                )

            elif search_field == "course_name":

                query = query.filter(
                    Course.course_name.ilike(
                        value
                    )
                )

        if department_id is not None:

            query = query.filter(
                Course.department_id == department_id
            )

        if level is not None:

            query = query.filter(
                Course.level == level
            )

        return (
            query.order_by(
                Course.course_name,
            )
            .all()
        )

    def exists(
        self,
        course_code: str,
    ) -> bool:
        """
        Determine whether a course exists.
        """

        return (
            self._session.query(
                func.count(
                    Course.course_code
                )
            )
            .filter(
                Course.course_code
                == course_code
            )
            .scalar()
            > 0
        )