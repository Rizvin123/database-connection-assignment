"""
Lecturer Qualification ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.lecturer import Lecturer


class LecturerQualification(Base, ReprMixin):
    """
    Represents a qualification held by a lecturer.
    """

    __tablename__ = "lecturer_qualifications"

    qualification_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    lecturer_id: Mapped[int] = mapped_column(
        ForeignKey("lecturers.lecturer_id"),
        nullable=False,
    )

    qualification_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    institution: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    year_awarded: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    lecturer: Mapped["Lecturer"] = relationship(
        back_populates="qualifications"
    )