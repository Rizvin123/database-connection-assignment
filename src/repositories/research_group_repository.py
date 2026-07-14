"""
Repository for Research Group operations.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.models.research_group import ResearchGroup
from src.repositories.base_repository import BaseRepository


class ResearchGroupRepository(
    BaseRepository[ResearchGroup]
):
    """
    Repository for ResearchGroup entities.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        """
        Initialise the repository.
        """

        super().__init__(
            session,
            ResearchGroup,
        )

    def get_research_groups(
        self,
    ) -> list[ResearchGroup]:
        """
        Retrieve all research groups ordered by name.
        """

        return (
            self._session.query(
                ResearchGroup,
            )
            .order_by(
                ResearchGroup.group_name,
            )
            .all()
        )

    def find_by_department(
        self,
        department_id: int,
    ) -> list[ResearchGroup]:
        """
        Retrieve research groups belonging to a department.
        """

        return (
            self._session.query(
                ResearchGroup,
            )
            .filter(
                ResearchGroup.department_id
                == department_id
            )
            .order_by(
                ResearchGroup.group_name,
            )
            .all()
        )