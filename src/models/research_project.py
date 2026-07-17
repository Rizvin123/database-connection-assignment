"""
Research Project ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.lecturer import Lecturer
    from src.models.research_project_publication import (
        ResearchProjectPublication,
    )
    from src.models.research_project_team import (
        ResearchProjectTeam,
    )


class ResearchProject(Base, ReprMixin):
    """
    Represents a university research project.
    """

    __tablename__ = "research_projects"

    project_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    project_title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    principal_investigator_id: Mapped[int] = mapped_column(
        ForeignKey("lecturers.lecturer_id"),
        nullable=False,
    )

    funding_source: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    outcomes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships

    principal_investigator: Mapped["Lecturer"] = relationship(
        back_populates="principal_investigator_projects",
    )

    team_members: Mapped[list["ResearchProjectTeam"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )

    publications: Mapped[list["ResearchProjectPublication"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )