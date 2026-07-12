"""
Program Course Requirement ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.course import Course
    from src.models.program import Program


class ProgramCourseRequirement(Base, ReprMixin):
    """
    Represents a course requirement within an academic program.
    """

    __tablename__ = "program_course_requirements"

    program_id: Mapped[int] = mapped_column(
        ForeignKey("programs.program_id"),
        primary_key=True,
    )

    course_code: Mapped[str] = mapped_column(
        ForeignKey("courses.course_code"),
        primary_key=True,
    )

    requirement_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Core",
    )

    recommended_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Relationships

    program: Mapped["Program"] = relationship(
        back_populates="course_requirements",
    )

    course: Mapped["Course"] = relationship(
        back_populates="program_requirements",
    )