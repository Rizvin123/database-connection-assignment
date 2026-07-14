"""
Tests for CourseRepository.
"""

from __future__ import annotations

import uuid

from src.models.course import Course
from src.repositories.course_repository import CourseRepository


def create_test_course() -> Course:
    """
    Create a Course object for testing.
    """

    unique = uuid.uuid4().hex[:8]

    return Course(
        course_code=f"TEST{unique}",
        course_name=f"Repository Test {unique}",
        description="Repository Test Course",
        department_id=1,
        level=1,
        credits=15,
        schedule="Monday 09:00-11:00",
    )


def test_create_course(session) -> None:
    """
    Verify create().
    """

    repository = CourseRepository(session)

    course = create_test_course()

    repository.create(course)

    assert course.course_code is not None

    repository.delete(course)


def test_get_course_by_id(session) -> None:
    """
    Verify get_by_id().
    """

    repository = CourseRepository(session)

    course = create_test_course()

    repository.create(course)

    found = repository.get_by_id(
        course.course_code,
    )

    assert found is not None

    assert (
        found.course_code
        == course.course_code
    )

    repository.delete(course)


def test_get_all_courses(session) -> None:
    """
    Verify get_all().
    """

    repository = CourseRepository(session)

    courses = repository.get_all()

    assert isinstance(
        courses,
        list,
    )


def test_save_course(session) -> None:
    """
    Verify save().
    """

    repository = CourseRepository(session)

    course = create_test_course()

    repository.create(course)

    course.schedule = "Friday 14:00-16:00"

    repository.save()

    updated = repository.get_by_id(
        course.course_code,
    )

    assert updated is not None

    assert (
        updated.schedule
        == "Friday 14:00-16:00"
    )

    repository.delete(course)


def test_delete_course(session) -> None:
    """
    Verify delete().
    """

    repository = CourseRepository(session)

    course = create_test_course()

    repository.create(course)

    course_code = course.course_code

    repository.delete(course)

    deleted = repository.get_by_id(
        course_code,
    )

    assert deleted is None


def test_find_by_course_name(session) -> None:
    """
    Verify find_by_course_name().
    """

    repository = CourseRepository(session)

    course = create_test_course()

    repository.create(course)

    found = repository.find_by_course_name(
        "Repository Test",
    )

    assert course in found

    repository.delete(course)


def test_find_by_department(session) -> None:
    """
    Verify find_by_department().
    """

    repository = CourseRepository(session)

    course = create_test_course()

    repository.create(course)

    found = repository.find_by_department(
        course.department_id,
    )

    assert course in found

    repository.delete(course)


def test_find_by_level(session) -> None:
    """
    Verify find_by_level().
    """

    repository = CourseRepository(session)

    course = create_test_course()

    repository.create(course)

    found = repository.find_by_level(
        course.level,
    )

    assert course in found

    repository.delete(course)


def test_search_courses(session) -> None:
    """
    Verify search_courses().
    """

    repository = CourseRepository(session)

    course = create_test_course()

    repository.create(course)

    found = repository.search_courses(
        search_field="course_code",
        search_text=course.course_code,
    )

    assert course in found

    repository.delete(course)


def test_exists(session) -> None:
    """
    Verify exists().
    """

    repository = CourseRepository(session)

    course = create_test_course()

    repository.create(course)

    assert repository.exists(
        course.course_code,
    )

    repository.delete(course)

    assert not repository.exists(
        course.course_code,
    )