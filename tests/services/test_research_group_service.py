"""
Tests for ResearchGroupService.
"""

from __future__ import annotations

import uuid

from src.models.research_group import ResearchGroup
from src.services.research_group_service import (
    ResearchGroupService,
)


def create_test_research_group() -> ResearchGroup:
    """
    Create a ResearchGroup object for testing.
    """

    unique = uuid.uuid4().hex[:8]

    return ResearchGroup(
        group_name=f"AI Research {unique}",
        department_id=1,
        head_lecturer_id=1,
    )


def test_create_research_group(session) -> None:
    """
    Verify create_research_group().
    """

    service = ResearchGroupService(session)

    group = create_test_research_group()

    created = service.create_research_group(
        group,
    )

    assert created.research_group_id is not None

    service.delete_research_group(
        created.research_group_id,
    )


def test_get_research_group(session) -> None:
    """
    Verify get_research_group().
    """

    service = ResearchGroupService(session)

    group = create_test_research_group()

    created = service.create_research_group(
        group,
    )

    found = service.get_research_group(
        created.research_group_id,
    )

    assert found is not None

    assert (
        found.research_group_id
        == created.research_group_id
    )

    service.delete_research_group(
        created.research_group_id,
    )


def test_get_all_research_groups(session) -> None:
    """
    Verify get_all_research_groups().
    """

    service = ResearchGroupService(session)

    groups = service.get_all_research_groups()

    assert isinstance(
        groups,
        list,
    )


def test_update_research_group(session) -> None:
    """
    Verify update_research_group().
    """

    service = ResearchGroupService(session)

    group = create_test_research_group()

    created = service.create_research_group(
        group,
    )

    created.group_name = (
        "Updated Research Group"
    )

    service.update_research_group()

    updated = service.get_research_group(
        created.research_group_id,
    )

    assert updated is not None

    assert (
        updated.group_name
        == "Updated Research Group"
    )

    service.delete_research_group(
        created.research_group_id,
    )


def test_delete_research_group(session) -> None:
    """
    Verify delete_research_group().
    """

    service = ResearchGroupService(session)

    group = create_test_research_group()

    created = service.create_research_group(
        group,
    )

    group_id = created.research_group_id

    deleted = service.delete_research_group(
        group_id,
    )

    assert deleted is True

    assert (
        service.get_research_group(
            group_id,
        )
        is None
    )


def test_find_by_name(session) -> None:
    """
    Verify find_by_name().
    """

    service = ResearchGroupService(session)

    group = create_test_research_group()

    created = service.create_research_group(
        group,
    )

    found = service.find_by_name(
        created.group_name,
    )

    assert found is not None

    assert (
        found.group_name
        == created.group_name
    )

    service.delete_research_group(
        created.research_group_id,
    )


def test_find_by_department(session) -> None:
    """
    Verify find_by_department().
    """

    service = ResearchGroupService(session)

    group = create_test_research_group()

    created = service.create_research_group(
        group,
    )

    found = service.find_by_department(
        created.department_id,
    )

    assert created in found

    service.delete_research_group(
        created.research_group_id,
    )


def test_find_by_head_lecturer(session) -> None:
    """
    Verify find_by_head_lecturer().
    """

    service = ResearchGroupService(session)

    group = create_test_research_group()

    created = service.create_research_group(
        group,
    )

    found = service.find_by_head_lecturer(
        created.head_lecturer_id,
    )

    assert created in found

    service.delete_research_group(
        created.research_group_id,
    )


def test_search_research_groups(session) -> None:
    """
    Verify search_research_groups().
    """

    service = ResearchGroupService(session)

    group = create_test_research_group()

    created = service.create_research_group(
        group,
    )

    found = service.search_research_groups(
        search_text=created.group_name,
    )

    assert created in found

    service.delete_research_group(
        created.research_group_id,
    )


def test_research_group_exists(session) -> None:
    """
    Verify research_group_exists().
    """

    service = ResearchGroupService(session)

    group = create_test_research_group()

    created = service.create_research_group(
        group,
    )

    assert service.research_group_exists(
        created.group_name,
    )

    service.delete_research_group(
        created.research_group_id,
    )

    assert not service.research_group_exists(
        created.group_name,
    )