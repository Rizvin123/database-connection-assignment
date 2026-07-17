"""
Disciplinary Record ORM model.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.student import Student


class DisciplinaryRecord(Base, ReprMixin):
    """
    Represents a disciplinary record for a student.
    """

    __tablename__ = "disciplinary_records"

    record_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.student_id"),
        nullable=False,
    )

    record_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    incident_type: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    action_taken: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships

    student: Mapped["Student"] = relationship(
        back_populates="disciplinary_records",
    )