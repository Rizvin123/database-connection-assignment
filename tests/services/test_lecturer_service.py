"""
Tests for LecturerService.
"""

from __future__ import annotations

import uuid

from src.models.lecturer import Lecturer
from src.services.lecturer_service import LecturerService


def create_test_lecturer() -> Lecturer:
    """
    Create a Lecturer object for testing.
    """

    return Lecturer(
        first_name="Service",
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
    Verify create_lecturer().
    """

    service = LecturerService(session)

    lecturer = create_test_lecturer()

    created = service.create_lecturer(
        lecturer,
    )

    assert created.lecturer_id is not None

    service.delete_lecturer(
        created.lecturer_id,
    )


def test_get_lecturer(session) -> None:
    """
    Verify get_lecturer().
    """

    service = LecturerService(session)

    lecturer = create_test_lecturer()

    created = service.create_lecturer(
        lecturer,
    )

    found = service.get_lecturer(
        created.lecturer_id,
    )

    assert found is not None

    assert (
        found.lecturer_id
        == created.lecturer_id
    )

    service.delete_lecturer(
        created.lecturer_id,
    )


def test_get_all_lecturers(session) -> None:
    """
    Verify get_all_lecturers().
    """

    service = LecturerService(session)

    lecturers = service.get_all_lecturers()

    assert isinstance(
        lecturers,
        list,
    )


def test_update_lecturer(session) -> None:
    """
    Verify update_lecturer().
    """

    service = LecturerService(session)

    lecturer = create_test_lecturer()

    created = service.create_lecturer(
        lecturer,
    )

    created.office_room = "B-205"

    service.update_lecturer()

    updated = service.get_lecturer(
        created.lecturer_id,
    )

    assert updated is not None

    assert updated.office_room == "B-205"

    service.delete_lecturer(
        created.lecturer_id,
    )


def test_delete_lecturer(session) -> None:
    """
    Verify delete_lecturer().
    """

    service = LecturerService(session)

    lecturer = create_test_lecturer()

    created = service.create_lecturer(
        lecturer,
    )

    lecturer_id = created.lecturer_id

    deleted = service.delete_lecturer(
        lecturer_id,
    )

    assert deleted is True

    assert (
        service.get_lecturer(
            lecturer_id,
        )
        is None
    )


def test_find_by_email(session) -> None:
    """
    Verify find_by_email().
    """

    service = LecturerService(session)

    lecturer = create_test_lecturer()

    created = service.create_lecturer(
        lecturer,
    )

    found = service.find_by_email(
        created.email,
    )

    assert found is not None

    assert found.email == created.email

    service.delete_lecturer(
        created.lecturer_id,
    )


def test_find_by_department(session) -> None:
    """
    Verify find_by_department().
    """

    service = LecturerService(session)

    lecturer = create_test_lecturer()

    created = service.create_lecturer(
        lecturer,
    )

    lecturers = service.find_by_department(
        created.department_id,
    )

    assert created in lecturers

    service.delete_lecturer(
        created.lecturer_id,
    )


def test_find_by_research_group(session) -> None:
    """
    Verify find_by_research_group().
    """

    service = LecturerService(session)

    lecturer = create_test_lecturer()

    created = service.create_lecturer(
        lecturer,
    )

    lecturers = service.find_by_research_group(
        created.research_group_id,
    )

    assert created in lecturers

    service.delete_lecturer(
        created.lecturer_id,
    )


def test_search_lecturers(session) -> None:
    """
    Verify search_lecturers().
    """

    service = LecturerService(session)

    lecturer = create_test_lecturer()

    created = service.create_lecturer(
        lecturer,
    )

    lecturers = service.search_lecturers(
        search_field="email",
        search_text=created.email,
    )

    assert created in lecturers

    service.delete_lecturer(
        created.lecturer_id,
    )