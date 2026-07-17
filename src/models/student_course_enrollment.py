"""
Student Course Enrollment ORM model.
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


class StudentCourseEnrollment(Base, ReprMixin):
    """
    Represents a student's enrollment in a course.
    """

    __tablename__ = "student_course_enrollments"

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.student_id"),
        primary_key=True,
    )

    course_code: Mapped[str] = mapped_column(
        ForeignKey("courses.course_code"),
        primary_key=True,
    )

    semester: Mapped[str] = mapped_column(
        String(30),
        primary_key=True,
    )

    academic_year: Mapped[str] = mapped_column(
        String(9),
        primary_key=True,
    )

    enrollment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    enrollment_status: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default="Enrolled",
    )

    final_grade: Mapped[float | None] = mapped_column(
        DECIMAL(5, 2),
        nullable=True,
    )

    # Relationships

    student: Mapped["Student"] = relationship(
        back_populates="enrollments",
    )

    course: Mapped["Course"] = relationship(
        back_populates="enrollments",
    )