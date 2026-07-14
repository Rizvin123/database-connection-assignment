"""
Tests for StudentService.
"""

from __future__ import annotations

import uuid
from datetime import date

import pytest

from src.models.student import Student
from src.repositories.student_repository import StudentRepository
from src.services.student_service import StudentService


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
        first_name="Service",
        last_name="Test",
        date_of_birth=date(2000, 1, 1),
        email=email or f"{uuid.uuid4()}@example.com",
        phone="9999999999",
        address="Test Address",
        program_id=program_id,
        year_of_study=year_of_study,
        graduation_status=graduation_status,
        advisor_lecturer_id=advisor_lecturer_id,
    )


def test_create_student(session) -> None:
    """
    Verify create_student().
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    student = create_test_student()

    created = service.create_student(student)

    assert created.student_id is not None

    repository.delete(created)


def test_create_student_duplicate_email(session) -> None:
    """
    Verify duplicate emails are rejected.
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    email = f"{uuid.uuid4()}@example.com"

    student_one = create_test_student(
        email=email,
    )

    student_two = create_test_student(
        email=email,
    )

    created = service.create_student(student_one)

    with pytest.raises(ValueError):
        service.create_student(student_two)

    repository.delete(created)


def test_get_student(session) -> None:
    """
    Verify get_student().
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    student = create_test_student()

    created = service.create_student(student)

    found = service.get_student(created.student_id)

    assert found is not None
    assert found.student_id == created.student_id

    repository.delete(created)


def test_delete_student(session) -> None:
    """
    Verify delete_student().
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    student = create_test_student()

    created = service.create_student(student)

    student_id = created.student_id

    service.delete_student(student_id)

    assert service.get_student(student_id) is None


def test_delete_nonexistent_student(session) -> None:
    """
    Verify deleting a nonexistent student raises an error.
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    with pytest.raises(ValueError):
        service.delete_student(-1)


def test_find_student_by_email(session) -> None:
    """
    Verify find_student_by_email().
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    email = f"{uuid.uuid4()}@example.com"

    student = create_test_student(
        email=email,
    )

    created = service.create_student(student)

    found = service.find_student_by_email(email)

    assert found is not None
    assert found.email == email

    repository.delete(created)


def test_find_students_by_program(session) -> None:
    """
    Verify find_students_by_program().
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    student = create_test_student(
        program_id=1,
    )

    created = service.create_student(student)

    students = service.find_students_by_program(1)

    assert created.student_id in [
        s.student_id
        for s in students
    ]

    repository.delete(created)


def test_find_students_by_advisor(session) -> None:
    """
    Verify find_students_by_advisor().
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    student = create_test_student(
        advisor_lecturer_id=1,
    )

    created = service.create_student(student)

    students = service.find_students_by_advisor(1)

    assert created.student_id in [
        s.student_id
        for s in students
    ]

    repository.delete(created)


def test_find_students_by_year(session) -> None:
    """
    Verify find_students_by_year().
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    student = create_test_student(
        year_of_study=3,
    )

    created = service.create_student(student)

    students = service.find_students_by_year(3)

    assert created.student_id in [
        s.student_id
        for s in students
    ]

    repository.delete(created)


def test_find_graduated_students(session) -> None:
    """
    Verify find_graduated_students().
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    student = create_test_student(
        graduation_status="Graduated",
    )

    created = service.create_student(student)

    students = service.find_graduated_students()

    assert created.student_id in [
        s.student_id
        for s in students
    ]

    repository.delete(created)

def test_search_students_by_first_name(session) -> None:
    """
    Verify searching students by first name.
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    student = create_test_student()
    student.first_name = "UniqueFirstName"

    created = service.create_student(student)

    results = service.search_students(
        search_field="first_name",
        search_text="UniqueFirstName",
    )

    assert created.student_id in [
        s.student_id
        for s in results
    ]

    repository.delete(created)

def test_search_students_by_last_name(session) -> None:
    """
    Verify searching students by last name.
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    student = create_test_student()
    student.last_name = "UniqueLastName"

    created = service.create_student(student)

    results = service.search_students(
        search_field="last_name",
        search_text="UniqueLastName",
    )

    assert created.student_id in [
        s.student_id
        for s in results
    ]

    repository.delete(created)

def test_search_students_by_email(session) -> None:
    """
    Verify searching students by email.
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    email = f"{uuid.uuid4()}@example.com"

    student = create_test_student(
        email=email,
    )

    created = service.create_student(student)

    results = service.search_students(
        search_field="email",
        search_text=email,
    )

    assert created.student_id in [
        s.student_id
        for s in results
    ]

    repository.delete(created)

def test_search_students_by_program(session) -> None:
    """
    Verify filtering students by program.
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    student = create_test_student(
        program_id=1,
    )

    created = service.create_student(student)

    results = service.search_students(
        program_id=1,
    )

    assert created.student_id in [
        s.student_id
        for s in results
    ]

    repository.delete(created)

def test_search_students_by_year(session) -> None:
    """
    Verify filtering students by year of study.
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    student = create_test_student(
        year_of_study=4,
    )

    created = service.create_student(student)

    results = service.search_students(
        year_of_study=4,
    )

    assert created.student_id in [
        s.student_id
        for s in results
    ]

    repository.delete(created)

def test_search_students_by_graduation_status(session) -> None:
    """
    Verify filtering students by graduation status.
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    student = create_test_student(
        graduation_status="Graduated",
    )

    created = service.create_student(student)

    results = service.search_students(
        graduation_status="Graduated",
    )

    assert created.student_id in [
        s.student_id
        for s in results
    ]

    repository.delete(created)

def test_search_students_combined_filters(session) -> None:
    """
    Verify searching students using multiple filters.
    """

    repository = StudentRepository(session)
    service = StudentService(repository)

    student = create_test_student(
        program_id=1,
        year_of_study=3,
    )

    student.first_name = "CombinedSearch"

    created = service.create_student(student)

    results = service.search_students(
        search_field="first_name",
        search_text="CombinedSearch",
        program_id=1,
        year_of_study=3,
    )

    assert created.student_id in [
        s.student_id
        for s in results
    ]

    repository.delete(created)