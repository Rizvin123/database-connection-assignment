"""
Student Grade ORM model.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, DECIMAL, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.course import Course
    from src.models.student import Student


class StudentGrade(Base, ReprMixin):
    """
    Represents an assessment grade earned by a student.
    """

    __tablename__ = "student_grades"

    grade_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.student_id"),
        nullable=False,
    )

    course_code: Mapped[str] = mapped_column(
        ForeignKey("courses.course_code"),
        nullable=False,
    )

    assessment_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    score: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    grade_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    # Relationships

    student: Mapped["Student"] = relationship(
        back_populates="grades",
    )

    course: Mapped["Course"] = relationship(
        back_populates="grades",
    )