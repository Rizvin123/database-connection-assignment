"""
Research Group ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.department import Department
    from src.models.lecturer import Lecturer


class ResearchGroup(Base, ReprMixin):
    """
    Represents a university research group.
    """

    __tablename__ = "research_groups"

    research_group_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    group_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.department_id"),
        nullable=False,
    )

    head_lecturer_id: Mapped[int | None] = mapped_column(
        ForeignKey("lecturers.lecturer_id"),
        nullable=True,
    )

    # Relationships

    department: Mapped["Department"] = relationship(
        back_populates="research_groups"
    )

    lecturers: Mapped[list["Lecturer"]] = relationship(
        back_populates="research_group",
        foreign_keys="Lecturer.research_group_id",
    )

    head_lecturer: Mapped["Lecturer | None"] = relationship(
        foreign_keys=[head_lecturer_id],
        post_update=True,
    )