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
    
    def find_by_name(
        self,
        group_name: str,
    ) -> ResearchGroup | None:
        """
        Retrieve a research group by name.
        """

        return (
            self._session.query(
                ResearchGroup,
            )
            .filter(
                ResearchGroup.group_name == group_name,
            )
            .first()
        )
    
    def find_by_head_lecturer(
        self,
        lecturer_id: int,
    ) -> list[ResearchGroup]:
        """
        Retrieve research groups headed by a lecturer.
        """

        return (
            self._session.query(
                ResearchGroup,
            )
            .filter(
                ResearchGroup.head_lecturer_id
                == lecturer_id,
            )
            .order_by(
                ResearchGroup.group_name,
            )
            .all()
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

        query = self._session.query(
            ResearchGroup,
        )

        if search_text:

            search_text = search_text.strip()

            query = query.filter(
                ResearchGroup.group_name.ilike(
                    f"%{search_text}%"
                )
            )

        if department_id is not None:

            query = query.filter(
                ResearchGroup.department_id
                == department_id,
            )

        if head_lecturer_id is not None:

            query = query.filter(
                ResearchGroup.head_lecturer_id
                == head_lecturer_id,
            )

        return (
            query.order_by(
                ResearchGroup.group_name,
            )
            .all()
        )
    
    def exists(
        self,
        group_name: str,
    ) -> bool:
        """
        Determine whether a research group exists.
        """

        return (
            self.find_by_name(
                group_name,
            )
            is not None
        )