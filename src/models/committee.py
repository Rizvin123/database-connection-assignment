"""
Committee ORM model.
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
    from src.models.department import Department
    from src.models.lecturer_committee_membership import (
        LecturerCommitteeMembership,
    )


class Committee(Base, ReprMixin):
    """
    Represents a university committee.
    """

    __tablename__ = "committees"

    committee_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    committee_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    department_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.department_id"),
        nullable=True,
    )

    # Relationships

    department: Mapped["Department | None"] = relationship(
        back_populates="committees",
    )

    members: Mapped[list["LecturerCommitteeMembership"]] = relationship(
        back_populates="committee",
        cascade="all, delete-orphan",
    )