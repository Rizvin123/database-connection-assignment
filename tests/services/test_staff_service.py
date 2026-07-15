"""
Tests for StaffService.
"""

from __future__ import annotations

import uuid

from src.models.staff import Staff
from src.services.staff_service import StaffService


def create_test_staff() -> Staff:
    """
    Create a Staff object for testing.
    """

    unique = uuid.uuid4().hex[:8]

    return Staff(
        first_name="John",
        last_name="Smith",
        email=f"john.smith.{unique}@example.com",
        phone="0123456789",
        job_title="Administrator",
        department_id=1,
        employment_type="Full-Time",
        contract_details="Permanent",
        salary=50000.00,
        emergency_contact_name="Jane Smith",
        emergency_contact_phone="0987654321",
    )


def test_create_staff(session) -> None:
    """
    Verify create_staff().
    """

    service = StaffService(session)

    staff = create_test_staff()

    created = service.create_staff(
        staff,
    )

    assert created.staff_id is not None

    service.delete_staff(
        created.staff_id,
    )


def test_get_staff(session) -> None:
    """
    Verify get_staff().
    """

    service = StaffService(session)

    staff = create_test_staff()

    created = service.create_staff(
        staff,
    )

    found = service.get_staff(
        created.staff_id,
    )

    assert found is not None

    assert (
        found.staff_id
        == created.staff_id
    )

    service.delete_staff(
        created.staff_id,
    )


def test_get_all_staff(session) -> None:
    """
    Verify get_all_staff().
    """

    service = StaffService(session)

    staff = service.get_all_staff()

    assert isinstance(
        staff,
        list,
    )


def test_update_staff(session) -> None:
    """
    Verify update_staff().
    """

    service = StaffService(session)

    staff = create_test_staff()

    created = service.create_staff(
        staff,
    )

    created.job_title = (
        "Senior Administrator"
    )

    service.update_staff()

    updated = service.get_staff(
        created.staff_id,
    )

    assert updated is not None

    assert (
        updated.job_title
        == "Senior Administrator"
    )

    service.delete_staff(
        created.staff_id,
    )


def test_delete_staff(session) -> None:
    """
    Verify delete_staff().
    """

    service = StaffService(session)

    staff = create_test_staff()

    created = service.create_staff(
        staff,
    )

    staff_id = created.staff_id

    deleted = service.delete_staff(
        staff_id,
    )

    assert deleted is True

    assert (
        service.get_staff(
            staff_id,
        )
        is None
    )


def test_find_by_email(session) -> None:
    """
    Verify find_by_email().
    """

    service = StaffService(session)

    staff = create_test_staff()

    created = service.create_staff(
        staff,
    )

    found = service.find_by_email(
        created.email,
    )

    assert found is not None

    assert (
        found.email
        == created.email
    )

    service.delete_staff(
        created.staff_id,
    )


def test_find_by_department(session) -> None:
    """
    Verify find_by_department().
    """

    service = StaffService(session)

    staff = create_test_staff()

    created = service.create_staff(
        staff,
    )

    found = service.find_by_department(
        created.department_id,
    )

    assert created in found

    service.delete_staff(
        created.staff_id,
    )


def test_find_by_job_title(session) -> None:
    """
    Verify find_by_job_title().
    """

    service = StaffService(session)

    staff = create_test_staff()

    created = service.create_staff(
        staff,
    )

    found = service.find_by_job_title(
        created.job_title,
    )

    assert created in found

    service.delete_staff(
        created.staff_id,
    )


def test_search_staff(session) -> None:
    """
    Verify search_staff().
    """

    service = StaffService(session)

    staff = create_test_staff()

    created = service.create_staff(
        staff,
    )

    found = service.search_staff(
        search_field="email",
        search_text=created.email,
    )

    assert created in found

    service.delete_staff(
        created.staff_id,
    )


def test_staff_exists(session) -> None:
    """
    Verify staff_exists().
    """

    service = StaffService(session)

    staff = create_test_staff()

    created = service.create_staff(
        staff,
    )

    assert service.staff_exists(
        created.email,
    )

    service.delete_staff(
        created.staff_id,
    )

    assert not service.staff_exists(
        created.email,
    )