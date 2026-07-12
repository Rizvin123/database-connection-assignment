"""
Lecturer Publication ORM model.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.lecturer import Lecturer


class LecturerPublication(Base, ReprMixin):
    """
    Represents a publication authored by a lecturer.
    """

    __tablename__ = "lecturer_publications"

    publication_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    lecturer_id: Mapped[int] = mapped_column(
        ForeignKey("lecturers.lecturer_id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    publication_type: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True,
    )

    journal_or_conference: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    publication_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    doi_or_reference: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    lecturer: Mapped["Lecturer"] = relationship(
        back_populates="publications"
    )