"""
Tests for CourseService.
"""

from __future__ import annotations

import uuid

from src.models.course import Course
from src.services.course_service import CourseService


def create_test_course() -> Course:
    """
    Create a Course object for testing.
    """

    unique = uuid.uuid4().hex[:8]

    return Course(
        course_code=f"TEST{unique}",
        course_name=f"Service Test {unique}",
        description="Service Test Course",
        department_id=1,
        level=1,
        credits=15,
        schedule="Monday 09:00-11:00",
    )


def test_create_course(session) -> None:
    """
    Verify create_course().
    """

    service = CourseService(session)

    course = create_test_course()

    created = service.create_course(
        course,
    )

    assert created.course_code is not None

    service.delete_course(
        created.course_code,
    )


def test_get_course(session) -> None:
    """
    Verify get_course().
    """

    service = CourseService(session)

    course = create_test_course()

    created = service.create_course(
        course,
    )

    found = service.get_course(
        created.course_code,
    )

    assert found is not None

    assert (
        found.course_code
        == created.course_code
    )

    service.delete_course(
        created.course_code,
    )


def test_get_all_courses(session) -> None:
    """
    Verify get_all_courses().
    """

    service = CourseService(session)

    courses = service.get_all_courses()

    assert isinstance(
        courses,
        list,
    )


def test_update_course(session) -> None:
    """
    Verify update_course().
    """

    service = CourseService(session)

    course = create_test_course()

    created = service.create_course(
        course,
    )

    created.schedule = "Friday 14:00-16:00"

    service.update_course()

    updated = service.get_course(
        created.course_code,
    )

    assert updated is not None

    assert (
        updated.schedule
        == "Friday 14:00-16:00"
    )

    service.delete_course(
        created.course_code,
    )


def test_delete_course(session) -> None:
    """
    Verify delete_course().
    """

    service = CourseService(session)

    course = create_test_course()

    created = service.create_course(
        course,
    )

    course_code = created.course_code

    deleted = service.delete_course(
        course_code,
    )

    assert deleted is True

    assert (
        service.get_course(
            course_code,
        )
        is None
    )


def test_find_by_course_name(session) -> None:
    """
    Verify find_by_course_name().
    """

    service = CourseService(session)

    course = create_test_course()

    created = service.create_course(
        course,
    )

    found = service.find_by_course_name(
        "Service Test",
    )

    assert created in found

    service.delete_course(
        created.course_code,
    )


def test_find_by_department(session) -> None:
    """
    Verify find_by_department().
    """

    service = CourseService(session)

    course = create_test_course()

    created = service.create_course(
        course,
    )

    found = service.find_by_department(
        created.department_id,
    )

    assert created in found

    service.delete_course(
        created.course_code,
    )


def test_find_by_level(session) -> None:
    """
    Verify find_by_level().
    """

    service = CourseService(session)

    course = create_test_course()

    created = service.create_course(
        course,
    )

    found = service.find_by_level(
        created.level,
    )

    assert created in found

    service.delete_course(
        created.course_code,
    )


def test_search_courses(session) -> None:
    """
    Verify search_courses().
    """

    service = CourseService(session)

    course = create_test_course()

    created = service.create_course(
        course,
    )

    found = service.search_courses(
        search_field="course_code",
        search_text=created.course_code,
    )

    assert created in found

    service.delete_course(
        created.course_code,
    )


def test_course_exists(session) -> None:
    """
    Verify course_exists().
    """

    service = CourseService(session)

    course = create_test_course()

    created = service.create_course(
        course,
    )

    assert service.course_exists(
        created.course_code,
    )

    service.delete_course(
        created.course_code,
    )

    assert not service.course_exists(
        created.course_code,
    )