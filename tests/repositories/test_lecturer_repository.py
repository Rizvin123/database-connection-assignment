"""
Tests for LecturerRepository.
"""

from __future__ import annotations

import uuid

from src.models.lecturer import Lecturer
from src.repositories.lecturer_repository import LecturerRepository


def create_test_lecturer() -> Lecturer:
    """
    Create a Lecturer object for testing.
    """

    return Lecturer(
        first_name="Repository",
        last_name="Test",
        email=f"{uuid.uuid4()}@example.com",
        phone="9999999999",
        department_id=1,
        course_load=2,
        research_group_id=1,
        office_room="A-101",
    )


def test_create_lecturer(session) -> None:
    """
    Verify create().
    """

    repository = LecturerRepository(session)

    lecturer = create_test_lecturer()

    repository.create(lecturer)

    assert lecturer.lecturer_id is not None

    repository.delete(lecturer)


def test_get_lecturer_by_id(session) -> None:
    """
    Verify get_by_id().
    """

    repository = LecturerRepository(session)

    lecturer = create_test_lecturer()

    repository.create(lecturer)

    found = repository.get_by_id(
        lecturer.lecturer_id,
    )

    assert found is not None

    assert (
        found.lecturer_id
        == lecturer.lecturer_id
    )

    repository.delete(lecturer)


def test_get_all_lecturers(session) -> None:
    """
    Verify get_all().
    """

    repository = LecturerRepository(session)

    lecturers = repository.get_all()

    assert isinstance(
        lecturers,
        list,
    )


def test_save_lecturer(session) -> None:
    """
    Verify save().
    """

    repository = LecturerRepository(session)

    lecturer = create_test_lecturer()

    repository.create(lecturer)

    lecturer.office_room = "B-205"

    repository.save()

    updated = repository.get_by_id(
        lecturer.lecturer_id,
    )

    assert updated is not None

    assert updated.office_room == "B-205"

    repository.delete(lecturer)


def test_delete_lecturer(session) -> None:
    """
    Verify delete().
    """

    repository = LecturerRepository(session)

    lecturer = create_test_lecturer()

    repository.create(lecturer)

    lecturer_id = lecturer.lecturer_id

    repository.delete(lecturer)

    deleted = repository.get_by_id(
        lecturer_id,
    )

    assert deleted is None


def test_find_by_email(session) -> None:
    """
    Verify find_by_email().
    """

    repository = LecturerRepository(session)

    lecturer = create_test_lecturer()

    repository.create(lecturer)

    found = repository.find_by_email(
        lecturer.email,
    )

    assert found is not None

    assert found.email == lecturer.email

    repository.delete(lecturer)


def test_find_by_department(session) -> None:
    """
    Verify find_by_department().
    """

    repository = LecturerRepository(session)

    lecturer = create_test_lecturer()

    repository.create(lecturer)

    lecturers = repository.find_by_department(
        lecturer.department_id,
    )

    assert lecturer in lecturers

    repository.delete(lecturer)


def test_find_by_research_group(session) -> None:
    """
    Verify find_by_research_group().
    """

    repository = LecturerRepository(session)

    lecturer = create_test_lecturer()

    repository.create(lecturer)

    lecturers = repository.find_by_research_group(
        lecturer.research_group_id,
    )

    assert lecturer in lecturers

    repository.delete(lecturer)


def test_search_lecturers(session) -> None:
    """
    Verify search_lecturers().
    """

    repository = LecturerRepository(session)

    lecturer = create_test_lecturer()

    repository.create(lecturer)

    lecturers = repository.search_lecturers(
        search_field="email",
        search_text=lecturer.email,
    )

    assert lecturer in lecturers

    repository.delete(lecturer)