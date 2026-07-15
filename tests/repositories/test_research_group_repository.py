"""
Tests for ResearchGroupRepository.
"""

from __future__ import annotations

import uuid

from src.models.research_group import ResearchGroup
from src.repositories.research_group_repository import (
    ResearchGroupRepository,
)


def create_test_research_group() -> ResearchGroup:
    """
    Create a research group for testing.
    """

    unique = uuid.uuid4().hex[:8]

    return ResearchGroup(
        group_name=f"AI Research {unique}",
        department_id=1,
        head_lecturer_id=1,
    )


def test_create_research_group(session) -> None:
    """
    Verify create().
    """

    repository = ResearchGroupRepository(session)

    group = create_test_research_group()

    repository.create(group)

    assert group.research_group_id is not None

    repository.delete(group)


def test_get_research_group_by_id(session) -> None:
    """
    Verify get_by_id().
    """

    repository = ResearchGroupRepository(session)

    group = create_test_research_group()

    repository.create(group)

    found = repository.get_by_id(
        group.research_group_id,
    )

    assert found is not None

    assert (
        found.research_group_id
        == group.research_group_id
    )

    repository.delete(group)


def test_get_research_groups(session) -> None:
    """
    Verify get_research_groups().
    """

    repository = ResearchGroupRepository(session)

    groups = repository.get_research_groups()

    assert isinstance(
        groups,
        list,
    )


def test_save_research_group(session) -> None:
    """
    Verify save().
    """

    repository = ResearchGroupRepository(session)

    group = create_test_research_group()

    repository.create(group)

    group.group_name = "Updated Research Group"

    repository.save()

    updated = repository.get_by_id(
        group.research_group_id,
    )

    assert updated is not None

    assert (
        updated.group_name
        == "Updated Research Group"
    )

    repository.delete(group)


def test_delete_research_group(session) -> None:
    """
    Verify delete().
    """

    repository = ResearchGroupRepository(session)

    group = create_test_research_group()

    repository.create(group)

    group_id = group.research_group_id

    repository.delete(group)

    assert (
        repository.get_by_id(group_id)
        is None
    )


def test_find_by_name(session) -> None:
    """
    Verify find_by_name().
    """

    repository = ResearchGroupRepository(session)

    group = create_test_research_group()

    repository.create(group)

    found = repository.find_by_name(
        group.group_name,
    )

    assert found is not None

    assert (
        found.group_name
        == group.group_name
    )

    repository.delete(group)


def test_find_by_department(session) -> None:
    """
    Verify find_by_department().
    """

    repository = ResearchGroupRepository(session)

    group = create_test_research_group()

    repository.create(group)

    groups = repository.find_by_department(
        group.department_id,
    )

    assert group in groups

    repository.delete(group)


def test_find_by_head_lecturer(session) -> None:
    """
    Verify find_by_head_lecturer().
    """

    repository = ResearchGroupRepository(session)

    group = create_test_research_group()

    repository.create(group)

    groups = repository.find_by_head_lecturer(
        group.head_lecturer_id,
    )

    assert group in groups

    repository.delete(group)


def test_search_research_groups(session) -> None:
    """
    Verify search_research_groups().
    """

    repository = ResearchGroupRepository(session)

    group = create_test_research_group()

    repository.create(group)

    results = repository.search_research_groups(
        search_text=group.group_name,
    )

    assert group in results

    repository.delete(group)


def test_exists(session) -> None:
    """
    Verify exists().
    """

    repository = ResearchGroupRepository(session)

    group = create_test_research_group()

    repository.create(group)

    assert repository.exists(
        group.group_name,
    )

    repository.delete(group)

    assert not repository.exists(
        group.group_name,
    )