"""
Repository for Student ORM operations.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.models.student import Student
from src.repositories.base_repository import BaseRepository


class StudentRepository(BaseRepository[Student]):
    """
    Repository providing Student-specific database operations.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        """
        Initialise the student repository.

        Parameters
        ----------
        session:
            SQLAlchemy database session.
        """

        super().__init__(
            session=session,
            model=Student,
        )

    def find_by_email(
        self,
        email: str,
    ) -> Student | None:
        """
        Find a student by email address.
        """

        return (
            self._session.query(Student)
            .filter(Student.email == email)
            .first()
        )

    def find_by_program(
        self,
        program_id: int,
    ) -> list[Student]:
        """
        Retrieve all students enrolled in a program.
        """

        return (
            self._session.query(Student)
            .filter(Student.program_id == program_id)
            .order_by(
                Student.last_name,
                Student.first_name,
            )
            .all()
        )

    def find_by_advisor(
        self,
        lecturer_id: int,
    ) -> list[Student]:
        """
        Retrieve all students advised by a lecturer.
        """

        return (
            self._session.query(Student)
            .filter(
                Student.advisor_lecturer_id == lecturer_id
            )
            .order_by(
                Student.last_name,
                Student.first_name,
            )
            .all()
        )

    def find_by_year_of_study(
        self,
        year: int,
    ) -> list[Student]:
        """
        Retrieve students in a specific year of study.
        """

        return (
            self._session.query(Student)
            .filter(
                Student.year_of_study == year
            )
            .order_by(
                Student.last_name,
                Student.first_name,
            )
            .all()
        )

    def find_graduated_students(
        self,
    ) -> list[Student]:
        """
        Retrieve all graduated students.
        """

        return (
            self._session.query(Student)
            .filter(
                Student.graduation_status == "Graduated"
            )
            .order_by(
                Student.last_name,
                Student.first_name,
            )
            .all()
        )