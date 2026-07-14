"""
Business logic for Student operations.
"""

from __future__ import annotations

from src.models.student import Student
from src.repositories.student_repository import StudentRepository


class StudentService:
    """
    Service layer for Student operations.
    """

    def __init__(
        self,
        repository: StudentRepository,
    ) -> None:
        """
        Initialise the service.

        Parameters
        ----------
        repository:
            Student repository.
        """

        self._repository = repository

    def create_student(
        self,
        student: Student,
    ) -> Student:
        """
        Create a student.

        Raises
        ------
        ValueError
            If the email address already exists.
        """

        existing = self._repository.find_by_email(
            student.email,
        )

        if existing is not None:
            raise ValueError(
                "A student with this email already exists."
            )

        return self._repository.create(student)

    def get_student(
        self,
        student_id: int,
    ) -> Student | None:
        """
        Retrieve a student by ID.
        """

        return self._repository.get_by_id(
            student_id,
        )

    def get_all_students(
        self,
    ) -> list[Student]:
        """
        Retrieve all students.
        """

        return self._repository.get_all()

    def update_student(
        self,
    ) -> None:
        """
        Save pending student changes.
        """

        self._repository.save()

    def delete_student(
        self,
        student_id: int,
    ) -> None:
        """
        Delete a student.

        Raises
        ------
        ValueError
            If the student does not exist.
        """

        student = self._repository.get_by_id(
            student_id,
        )

        if student is None:
            raise ValueError(
                "Student not found."
            )

        self._repository.delete(student)

    def find_student_by_email(
        self,
        email: str,
    ) -> Student | None:
        """
        Retrieve a student by email.
        """

        return self._repository.find_by_email(
            email,
        )

    def find_students_by_program(
        self,
        program_id: int,
    ) -> list[Student]:
        """
        Retrieve students in a program.
        """

        return self._repository.find_by_program(
            program_id,
        )

    def find_students_by_advisor(
        self,
        lecturer_id: int,
    ) -> list[Student]:
        """
        Retrieve students advised by a lecturer.
        """

        return self._repository.find_by_advisor(
            lecturer_id,
        )

    def find_students_by_year(
        self,
        year: int,
    ) -> list[Student]:
        """
        Retrieve students by year of study.
        """

        return self._repository.find_by_year_of_study(
            year,
        )

    def find_graduated_students(
        self,
    ) -> list[Student]:
        """
        Retrieve graduated students.
        """

        return self._repository.find_graduated_students()
    
    def search_students(
        self,
        *,
        search_field: str | None = None,
        search_text: str | None = None,
        program_id: int | None = None,
        year_of_study: int | None = None,
        graduation_status: str | None = None,
    ) -> list[Student]:
        """
        Search students.
        """

        return self._repository.search_students(
            search_field=search_field,
            search_text=search_text,
            program_id=program_id,
            year_of_study=year_of_study,
            graduation_status=graduation_status,
        )