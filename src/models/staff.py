"""
Staff ORM model.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL
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
    from src.models.research_project_team import ResearchProjectTeam


class Staff(Base, ReprMixin):
    """
    Represents a non-academic staff member.
    """

    __tablename__ = "staff"

    staff_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    first_name: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(120),
        unique=True,
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    job_title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.department_id"),
        nullable=False,
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    contract_details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    salary: Mapped[Decimal | None] = mapped_column(
        DECIMAL(10, 2),
        nullable=True,
    )

    emergency_contact_name: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    emergency_contact_phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    # Relationships

    department: Mapped["Department"] = relationship(
        back_populates="staff_members",
    )

    research_projects: Mapped[list["ResearchProjectTeam"]] = relationship(
        back_populates="staff",
        cascade="all, delete-orphan",
    )