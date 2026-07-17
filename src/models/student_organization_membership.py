"""
Student Organization Membership ORM model.
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
    from src.models.student import Student
    from src.models.student_organization import StudentOrganization


class StudentOrganizationMembership(Base, ReprMixin):
    """
    Represents a student's membership in an organization.
    """

    __tablename__ = "student_organization_memberships"

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.student_id"),
        primary_key=True,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("student_organizations.organization_id"),
        primary_key=True,
    )

    join_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    role_in_organization: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True,
    )

    # Relationships

    student: Mapped["Student"] = relationship(
        back_populates="organization_memberships",
    )

    organization: Mapped["StudentOrganization"] = relationship(
        back_populates="memberships",
    )