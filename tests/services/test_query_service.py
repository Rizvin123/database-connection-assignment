"""
Tests for QueryService.
"""

from __future__ import annotations

from src.services.query_service import QueryService

def test_students_by_course_and_lecturer(
    session,
) -> None:
    """
    Verify Query 1 executes successfully.
    """

    service = QueryService(
        session,
    )

    results = (
        service.students_by_course_and_lecturer(
            course_code="CS101",
            lecturer_id=1,
            semester="Semester 1",
            academic_year="2025/2026",
        )
    )

    assert isinstance(
        results,
        list,
    )

def test_final_year_students_above_average(
    session,
) -> None:
    """
    Verify Query 2 executes successfully.
    """

    service = QueryService(
        session,
    )

    results = (
        service.final_year_students_above_average(
            minimum_average=70,
        )
    )

    assert isinstance(
        results,
        list,
    )

def test_students_not_enrolled(
    session,
) -> None:
    """
    Verify Query 3 executes successfully.
    """

    service = QueryService(
        session,
    )

    results = (
        service.students_not_enrolled(
            semester="Semester 1",
            academic_year="2025/2026",
        )
    )

    assert isinstance(
        results,
        list,
    )

def test_faculty_advisor_details(
    session,
) -> None:
    """
    Verify Query 4 executes successfully.
    """

    service = QueryService(
        session,
    )

    result = (
        service.faculty_advisor_details(
            student_id=1,
        )
    )

    assert (
        result is None
        or isinstance(
            result,
            tuple,
        )
    )

def test_lecturers_by_research_area(
    session,
) -> None:
    """
    Verify Query 5 executes successfully.
    """

    service = QueryService(
        session,
    )

    results = (
        service.lecturers_by_research_area(
            "Database",
        )
    )

    assert isinstance(
        results,
        list,
    )