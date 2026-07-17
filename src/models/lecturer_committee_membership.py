"""
Lecturer Committee Membership ORM model.
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
    from src.models.committee import Committee
    from src.models.lecturer import Lecturer


class LecturerCommitteeMembership(Base, ReprMixin):
    """
    Represents a lecturer's membership on a committee.
    """

    __tablename__ = "lecturer_committee_memberships"

    lecturer_id: Mapped[int] = mapped_column(
        ForeignKey("lecturers.lecturer_id"),
        primary_key=True,
    )

    committee_id: Mapped[int] = mapped_column(
        ForeignKey("committees.committee_id"),
        primary_key=True,
    )

    role_on_committee: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True,
    )

    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Relationships

    lecturer: Mapped["Lecturer"] = relationship(
        back_populates="committee_memberships",
    )

    committee: Mapped["Committee"] = relationship(
        back_populates="members",
    )