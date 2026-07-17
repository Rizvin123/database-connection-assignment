"""
Service layer for Course operations.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.models.course import Course
from src.repositories.course_repository import CourseRepository


class CourseService:
    """
    Service layer for Course business logic.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        """
        Initialise the service.
        """

        self._repository = CourseRepository(
            session,
        )

    def create_course(
        self,
        course: Course,
    ) -> Course:
        """
        Create a course.
        """

        return self._repository.create(
            course,
        )

    def get_course(
        self,
        course_code: str,
    ) -> Course | None:
        """
        Retrieve a course by course code.
        """

        return self._repository.get_by_id(
            course_code,
        )

    def get_all_courses(
        self,
    ) -> list[Course]:
        """
        Retrieve all courses.
        """

        return self._repository.get_all()

    def update_course(
        self,
    ) -> None:
        """
        Persist pending course changes.
        """

        self._repository.save()

    def delete_course(
        self,
        course_code: str,
    ) -> bool:
        """
        Delete a course.
        """

        course = self.get_course(
            course_code,
        )

        if course is None:

            return False

        self._repository.delete(
            course,
        )

        return True

    def find_by_course_name(
        self,
        course_name: str,
    ) -> list[Course]:
        """
        Find courses by course name.
        """

        return self._repository.find_by_course_name(
            course_name,
        )

    def find_by_department(
        self,
        department_id: int,
    ) -> list[Course]:
        """
        Retrieve courses belonging to a department.
        """

        return self._repository.find_by_department(
            department_id,
        )

    def find_by_level(
        self,
        level: int,
    ) -> list[Course]:
        """
        Retrieve courses for a level.
        """

        return self._repository.find_by_level(
            level,
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

        return self._repository.search_courses(
            search_field=search_field,
            search_text=search_text,
            department_id=department_id,
            level=level,
        )

    def course_exists(
        self,
        course_code: str,
    ) -> bool:
        """
        Determine whether a course exists.
        """

        return self._repository.exists(
            course_code,
        )