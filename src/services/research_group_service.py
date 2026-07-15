"""
Service layer for Research Group operations.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.models.research_group import ResearchGroup
from src.repositories.research_group_repository import (
    ResearchGroupRepository,
)


class ResearchGroupService:
    """
    Service layer for Research Group business logic.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        """
        Initialise the service.
        """

        self._repository = ResearchGroupRepository(
            session,
        )

    def create_research_group(
        self,
        research_group: ResearchGroup,
    ) -> ResearchGroup:
        """
        Create a research group.
        """

        return self._repository.create(
            research_group,
        )

    def get_research_group(
        self,
        research_group_id: int,
    ) -> ResearchGroup | None:
        """
        Retrieve a research group by ID.
        """

        return self._repository.get_by_id(
            research_group_id,
        )

    def get_all_research_groups(
        self,
    ) -> list[ResearchGroup]:
        """
        Retrieve all research groups.
        """

        return self._repository.get_research_groups()

    def update_research_group(
        self,
    ) -> None:
        """
        Persist pending research group changes.
        """

        self._repository.save()

    def delete_research_group(
        self,
        research_group_id: int,
    ) -> bool:
        """
        Delete a research group.
        """

        research_group = self.get_research_group(
            research_group_id,
        )

        if research_group is None:

            return False

        self._repository.delete(
            research_group,
        )

        return True

    def find_by_name(
        self,
        group_name: str,
    ) -> ResearchGroup | None:
        """
        Find a research group by name.
        """

        return self._repository.find_by_name(
            group_name,
        )

    def find_by_department(
        self,
        department_id: int,
    ) -> list[ResearchGroup]:
        """
        Retrieve research groups in a department.
        """

        return self._repository.find_by_department(
            department_id,
        )

    def find_by_head_lecturer(
        self,
        lecturer_id: int,
    ) -> list[ResearchGroup]:
        """
        Retrieve research groups headed by a lecturer.
        """

        return self._repository.find_by_head_lecturer(
            lecturer_id,
        )

    def search_research_groups(
        self,
        *,
        search_text: str | None = None,
        department_id: int | None = None,
        head_lecturer_id: int | None = None,
    ) -> list[ResearchGroup]:
        """
        Search research groups using optional filters.
        """

        return self._repository.search_research_groups(
            search_text=search_text,
            department_id=department_id,
            head_lecturer_id=head_lecturer_id,
        )

    def research_group_exists(
        self,
        group_name: str,
    ) -> bool:
        """
        Determine whether a research group exists.
        """

        return self._repository.exists(
            group_name,
        )