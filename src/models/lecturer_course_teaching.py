"""
Lecturer Course Teaching ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.course import Course
    from src.models.lecturer import Lecturer


class LecturerCourseTeaching(Base, ReprMixin):
    """
    Represents a lecturer teaching a course during a semester.
    """

    __tablename__ = "lecturer_course_teaching"

    lecturer_id: Mapped[int] = mapped_column(
        ForeignKey("lecturers.lecturer_id"),
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

    teaching_role: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True,
    )

    # Relationships

    lecturer: Mapped["Lecturer"] = relationship(
        back_populates="teaching_assignments",
    )

    course: Mapped["Course"] = relationship(
        back_populates="teaching_assignments",
    )