"""
Program ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.department import Department
    from src.models.student import Student
    from src.models.program_course_requirement import ProgramCourseRequirement


class Program(Base, ReprMixin):
    """
    Represents an academic program.
    """

    __tablename__ = "programs"

    program_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    program_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    degree_awarded: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    duration_years: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.department_id"),
        nullable=False,
    )

    enrolment_details: Mapped[str | None] = mapped_column(
        Text
    )

    # Relationships

    department: Mapped["Department"] = relationship(
        back_populates="programs"
    )

    students: Mapped[list["Student"]] = relationship(
        back_populates="program"
    )

    course_requirements: Mapped[list["ProgramCourseRequirement"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan",
    )