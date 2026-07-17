"""
Student Organization ORM model.
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
    from src.models.student_organization_membership import (
        StudentOrganizationMembership,
    )


class StudentOrganization(Base, ReprMixin):
    """
    Represents a student organization.
    """

    __tablename__ = "student_organizations"

    organization_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    organization_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
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
        back_populates="student_organizations",
    )

    memberships: Mapped[list["StudentOrganizationMembership"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
    )