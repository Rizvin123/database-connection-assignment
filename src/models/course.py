"""
Course ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.course_material import CourseMaterial
    from src.models.course_prerequisite import CoursePrerequisite
    from src.models.department import Department
    from src.models.lecturer_course_teaching import LecturerCourseTeaching
    from src.models.program_course_requirement import (
        ProgramCourseRequirement,
    )
    from src.models.student_course_enrollment import (
        StudentCourseEnrollment,
    )
    from src.models.student_grade import StudentGrade


class Course(Base, ReprMixin):
    """
    Represents a university course.
    """

    __tablename__ = "courses"

    course_code: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
    )

    course_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.department_id"),
        nullable=False,
    )

    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    credits: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    schedule: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    # Relationships

    department: Mapped["Department"] = relationship(
        back_populates="courses"
    )

    materials: Mapped[list["CourseMaterial"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
    )

    prerequisites: Mapped[list["CoursePrerequisite"]] = relationship(
        foreign_keys="CoursePrerequisite.course_code",
        back_populates="course",
        cascade="all, delete-orphan",
    )

    prerequisite_for: Mapped[list["CoursePrerequisite"]] = relationship(
        foreign_keys="CoursePrerequisite.prerequisite_course_code",
        back_populates="prerequisite_course",
        cascade="all, delete-orphan",
    )

    program_requirements: Mapped[
        list["ProgramCourseRequirement"]
    ] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
    )

    teaching_assignments: Mapped[
        list["LecturerCourseTeaching"]
    ] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
    )

    enrollments: Mapped[
        list["StudentCourseEnrollment"]
    ] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
    )

    grades: Mapped[list["StudentGrade"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
    )