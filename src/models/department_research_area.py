"""
Department Research Area ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.department import Department


class DepartmentResearchArea(Base, ReprMixin):
    """
    Represents a research area belonging to a department.
    """

    __tablename__ = "department_research_areas"

    department_research_area_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.department_id"),
        nullable=False,
    )

    research_area: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    # Relationships

    department: Mapped["Department"] = relationship(
        back_populates="research_areas"
    )