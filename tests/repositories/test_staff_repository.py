"""
Tests for StaffRepository.
"""

from __future__ import annotations

import uuid

from src.models.staff import Staff
from src.repositories.staff_repository import StaffRepository


def create_test_staff() -> Staff:
    """
    Create a test staff member.
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
    Verify create().
    """

    repository = StaffRepository(session)

    staff = create_test_staff()

    repository.create(staff)

    assert staff.staff_id is not None

    repository.delete(staff)


def test_get_staff_by_id(session) -> None:
    """
    Verify get_by_id().
    """

    repository = StaffRepository(session)

    staff = create_test_staff()

    repository.create(staff)

    found = repository.get_by_id(
        staff.staff_id,
    )

    assert found is not None

    assert found.staff_id == staff.staff_id

    repository.delete(staff)


def test_save_staff(session) -> None:
    """
    Verify save().
    """

    repository = StaffRepository(session)

    staff = create_test_staff()

    repository.create(staff)

    staff.first_name = "Updated"

    repository.save()

    updated = repository.get_by_id(
        staff.staff_id,
    )

    assert updated is not None

    assert updated.first_name == "Updated"

    repository.delete(staff)


def test_delete_staff(session) -> None:
    """
    Verify delete().
    """

    repository = StaffRepository(session)

    staff = create_test_staff()

    repository.create(staff)

    staff_id = staff.staff_id

    repository.delete(staff)

    assert repository.get_by_id(staff_id) is None


def test_find_by_email(session) -> None:
    """
    Verify find_by_email().
    """

    repository = StaffRepository(session)

    staff = create_test_staff()

    repository.create(staff)

    found = repository.find_by_email(
        staff.email,
    )

    assert found is not None

    assert found.email == staff.email

    repository.delete(staff)


def test_find_by_department(session) -> None:
    """
    Verify find_by_department().
    """

    repository = StaffRepository(session)

    staff = create_test_staff()

    repository.create(staff)

    staff_members = repository.find_by_department(
        staff.department_id,
    )

    assert staff in staff_members

    repository.delete(staff)


def test_find_by_job_title(session) -> None:
    """
    Verify find_by_job_title().
    """

    repository = StaffRepository(session)

    staff = create_test_staff()

    repository.create(staff)

    staff_members = repository.find_by_job_title(
        staff.job_title,
    )

    assert staff in staff_members

    repository.delete(staff)


def test_search_staff(session) -> None:
    """
    Verify search_staff().
    """

    repository = StaffRepository(session)

    staff = create_test_staff()

    repository.create(staff)

    results = repository.search_staff(
        search_field="email",
        search_text=staff.email,
    )

    assert staff in results

    repository.delete(staff)


def test_exists(session) -> None:
    """
    Verify exists().
    """

    repository = StaffRepository(session)

    staff = create_test_staff()

    repository.create(staff)

    assert repository.exists(staff.email)

    repository.delete(staff)

    assert not repository.exists(staff.email)