"""
Department ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.course import Course
    from src.models.department_research_area import DepartmentResearchArea
    from src.models.lecturer import Lecturer
    from src.models.program import Program
    from src.models.research_group import ResearchGroup
    from src.models.staff import Staff
    from src.models.committee import Committee
    from src.models.student_organization import StudentOrganization


class Department(Base, ReprMixin):
    """
    Represents a university department.
    """

    __tablename__ = "departments"

    department_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    department_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    faculty_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    office_location: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(120),
        unique=True,
        nullable=True,
    )

    # Relationships

    programs: Mapped[list["Program"]] = relationship(
        back_populates="department"
    )

    lecturers: Mapped[list["Lecturer"]] = relationship(
        back_populates="department"
    )

    staff_members: Mapped[list["Staff"]] = relationship(
        back_populates="department"
    )

    research_groups: Mapped[list["ResearchGroup"]] = relationship(
        back_populates="department"
    )

    courses: Mapped[list["Course"]] = relationship(
        back_populates="department"
    )

    research_areas: Mapped[list["DepartmentResearchArea"]] = relationship(
        back_populates="department",
        cascade="all, delete-orphan",
    )

    committees: Mapped[list["Committee"]] = relationship(
        back_populates="department"
    )

    student_organizations: Mapped[list["StudentOrganization"]] = relationship(
        back_populates="department"
    )