"""
Lecturer Research Interest ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.lecturer import Lecturer


class LecturerResearchInterest(Base, ReprMixin):
    """
    Represents a research interest of a lecturer.
    """

    __tablename__ = "lecturer_research_interests"

    interest_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    lecturer_id: Mapped[int] = mapped_column(
        ForeignKey("lecturers.lecturer_id"),
        nullable=False,
    )

    research_interest: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    lecturer: Mapped["Lecturer"] = relationship(
        back_populates="research_interests"
    )