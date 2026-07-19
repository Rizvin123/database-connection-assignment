"""
Tests for the generic BaseRepository.
"""
from __future__ import annotations
import uuid

from datetime import date

from sqlalchemy import inspect

from src.models.student import Student
from src.repositories.base_repository import BaseRepository


def create_test_student() -> Student:
    """
    Create a Student object for testing.
    """

    return Student(
        first_name="Repository",
        last_name="Test",
        date_of_birth=date(2000, 1, 1),
        email=f"{uuid.uuid4()}@example.com",
        phone="9999999999",
        address="Test Address",
        program_id=1,
        year_of_study=1,
        graduation_status="Not Graduated",
        advisor_lecturer_id=1,
    )


def test_create_student(session) -> None:
    """
    Verify create().
    """

    repository = BaseRepository(session, Student)

    student = create_test_student()

    repository.create(student)

    assert student.student_id is not None

    repository.delete(student)


def test_get_student_by_id(session) -> None:
    """
    Verify get_by_id().
    """

    repository = BaseRepository(session, Student)

    student = create_test_student()

    repository.create(student)

    found = repository.get_by_id(student.student_id)

    assert found is not None
    assert found.student_id == student.student_id

    repository.delete(student)


def test_get_all_students(session) -> None:
    """
    Verify get_all().
    """

    repository = BaseRepository(session, Student)

    students = repository.get_all()

    assert isinstance(students, list)


def test_save_student(session) -> None:
    """
    Verify save().
    """

    repository = BaseRepository(session, Student)

    student = create_test_student()

    repository.create(student)

    student.phone = "1234567890"

    repository.save()

    assert inspect(student).expired

    updated = repository.get_by_id(student.student_id)

    assert updated.phone == "1234567890"

    repository.delete(student)


def test_delete_student(session) -> None:
    """
    Verify delete().
    """

    repository = BaseRepository(session, Student)

    student = create_test_student()

    repository.create(student)

    student_id = student.student_id

    repository.delete(student)

    deleted = repository.get_by_id(student_id)

    assert deleted is None
