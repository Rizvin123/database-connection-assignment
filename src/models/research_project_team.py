"""
Research Project Team ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.lecturer import Lecturer
    from src.models.research_project import ResearchProject
    from src.models.staff import Staff


class ResearchProjectTeam(Base, ReprMixin):
    """
    Represents a member of a research project team.
    """

    __tablename__ = "research_project_team"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("research_projects.project_id"),
        primary_key=True,
    )

    lecturer_id: Mapped[int | None] = mapped_column(
        ForeignKey("lecturers.lecturer_id"),
        primary_key=True,
        nullable=True,
    )

    staff_id: Mapped[int | None] = mapped_column(
        ForeignKey("staff.staff_id"),
        primary_key=True,
        nullable=True,
    )

    project_role: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Relationships

    project: Mapped["ResearchProject"] = relationship(
        back_populates="team_members",
    )

    lecturer: Mapped["Lecturer | None"] = relationship(
        back_populates="research_projects",
    )

    staff: Mapped["Staff | None"] = relationship(
        back_populates="research_projects",
    )