"""
Research Project Publication ORM model.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.research_project import ResearchProject


class ResearchProjectPublication(Base, ReprMixin):
    """
    Represents a publication resulting from a research project.
    """

    __tablename__ = "research_project_publications"

    publication_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("research_projects.project_id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    publication_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    publication_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Relationships

    project: Mapped["ResearchProject"] = relationship(
        back_populates="publications",
    )