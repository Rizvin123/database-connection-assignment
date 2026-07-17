"""
Tests for StudentRepository.
"""

from __future__ import annotations

import uuid
from datetime import date

from src.models.student import Student
from src.repositories.student_repository import StudentRepository


def create_test_student(
    *,
    email: str | None = None,
    program_id: int = 1,
    advisor_lecturer_id: int = 1,
    year_of_study: int = 1,
    graduation_status: str = "Not Graduated",
) -> Student:
    """
    Create a Student object for testing.
    """

    return Student(
        first_name="Repository",
        last_name="Student",
        date_of_birth=date(2000, 1, 1),
        email=email or f"{uuid.uuid4()}@example.com",
        phone="9999999999",
        address="Test Address",
        program_id=program_id,
        year_of_study=year_of_study,
        graduation_status=graduation_status,
        advisor_lecturer_id=advisor_lecturer_id,
    )


def test_find_by_email(session) -> None:
    """
    Verify find_by_email().
    """

    repository = StudentRepository(session)

    email = f"{uuid.uuid4()}@example.com"

    student = create_test_student(
        email=email,
    )

    repository.create(student)

    found = repository.find_by_email(email)

    assert found is not None
    assert found.email == email

    repository.delete(student)


def test_find_by_program(session) -> None:
    """
    Verify find_by_program().
    """

    repository = StudentRepository(session)

    student = create_test_student(
        program_id=1,
    )

    repository.create(student)

    students = repository.find_by_program(1)

    assert student.student_id in [
        s.student_id
        for s in students
    ]

    repository.delete(student)


def test_find_by_advisor(session) -> None:
    """
    Verify find_by_advisor().
    """

    repository = StudentRepository(session)

    student = create_test_student(
        advisor_lecturer_id=1,
    )

    repository.create(student)

    students = repository.find_by_advisor(1)

    assert student.student_id in [
        s.student_id
        for s in students
    ]

    repository.delete(student)


def test_find_by_year_of_study(session) -> None:
    """
    Verify find_by_year_of_study().
    """

    repository = StudentRepository(session)

    student = create_test_student(
        year_of_study=3,
    )

    repository.create(student)

    students = repository.find_by_year_of_study(3)

    assert student.student_id in [
        s.student_id
        for s in students
    ]

    repository.delete(student)


def test_find_graduated_students(session) -> None:
    """
    Verify find_graduated_students().
    """

    repository = StudentRepository(session)

    student = create_test_student(
        graduation_status="Graduated",
    )

    repository.create(student)

    students = repository.find_graduated_students()

    assert student.student_id in [
        s.student_id
        for s in students
    ]

    repository.delete(student)

def test_search_by_first_name(session) -> None:
    """
    Verify searching by first name.
    """

    repository = StudentRepository(session)

    student = create_test_student()

    student.first_name = "UniqueFirstName"

    repository.create(student)

    results = repository.search_students(
        search_field="first_name",
        search_text="UniqueFirstName",
    )

    assert student.student_id in [
        s.student_id for s in results
    ]

    repository.delete(student)

def test_search_by_last_name(session) -> None:
    """
    Verify searching by last name.
    """

    repository = StudentRepository(session)

    student = create_test_student()

    student.last_name = "UniqueLastName"

    repository.create(student)

    results = repository.search_students(
        search_field="last_name",
        search_text="UniqueLastName",
    )

    assert student.student_id in [
        s.student_id for s in results
    ]

    repository.delete(student)

def test_search_by_email(session) -> None:
    """
    Verify searching by email.
    """

    repository = StudentRepository(session)

    email = f"{uuid.uuid4()}@example.com"

    student = create_test_student(
        email=email,
    )

    repository.create(student)

    results = repository.search_students(
        search_field="email",
        search_text=email,
    )

    assert student.student_id in [
        s.student_id for s in results
    ]

    repository.delete(student)

def test_search_by_program(session) -> None:
    """
    Verify filtering by program.
    """

    repository = StudentRepository(session)

    student = create_test_student(
        program_id=1,
    )

    repository.create(student)

    results = repository.search_students(
        program_id=1,
    )

    assert student.student_id in [
        s.student_id for s in results
    ]

    repository.delete(student)

def test_search_by_year(session) -> None:
    """
    Verify filtering by year.
    """

    repository = StudentRepository(session)

    student = create_test_student(
        year_of_study=4,
    )

    repository.create(student)

    results = repository.search_students(
        year_of_study=4,
    )

    assert student.student_id in [
        s.student_id for s in results
    ]

    repository.delete(student)

def test_search_by_graduation_status(session) -> None:
    """
    Verify filtering by graduation status.
    """

    repository = StudentRepository(session)

    student = create_test_student(
        graduation_status="Graduated",
    )

    repository.create(student)

    results = repository.search_students(
        graduation_status="Graduated",
    )

    assert student.student_id in [
        s.student_id for s in results
    ]

    repository.delete(student)

def test_search_combined_filters(session) -> None:
    """
    Verify multiple search filters together.
    """

    repository = StudentRepository(session)

    student = create_test_student(
        program_id=1,
        year_of_study=3,
    )

    student.first_name = "CombinedSearch"

    repository.create(student)

    results = repository.search_students(
        search_field="first_name",
        search_text="CombinedSearch",
        program_id=1,
        year_of_study=3,
    )

    assert len(results) >= 1

    assert student.student_id in [
        s.student_id for s in results
    ]

    repository.delete(student)