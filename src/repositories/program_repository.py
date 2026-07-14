"""
Repository for Program ORM operations.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.models.program import Program
from src.repositories.base_repository import BaseRepository


class ProgramRepository(BaseRepository[Program]):
    """
    Repository providing Program-specific database operations.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=Program,
        )

    def get_program_names(
        self,
    ) -> list[Program]:
        """
        Retrieve all programs ordered by program name.
        """

        return (
            self._session.query(Program)
            .order_by(Program.program_name)
            .all()
        )