"""
Student ORM model.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.disciplinary_record import DisciplinaryRecord
    from src.models.lecturer import Lecturer
    from src.models.program import Program
    from src.models.student_course_enrollment import StudentCourseEnrollment
    from src.models.student_grade import StudentGrade
    from src.models.student_organization_membership import (
        StudentOrganizationMembership,
    )


class Student(Base, ReprMixin):
    """
    Represents a university student.
    """

    __tablename__ = "students"

    student_id: Mapped[int] = mapped_column(
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

    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
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

    address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    program_id: Mapped[int] = mapped_column(
        ForeignKey("programs.program_id"),
        nullable=False,
    )

    year_of_study: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    graduation_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Not Graduated",
    )

    advisor_lecturer_id: Mapped[int | None] = mapped_column(
        ForeignKey("lecturers.lecturer_id"),
        nullable=True,
    )

    # Relationships

    program: Mapped["Program"] = relationship(
        back_populates="students"
    )

    advisor: Mapped["Lecturer | None"] = relationship(
        back_populates="advised_students"
    )

    grades: Mapped[list["StudentGrade"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
    )

    enrollments: Mapped[list["StudentCourseEnrollment"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
    )

    disciplinary_records: Mapped[list["DisciplinaryRecord"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
    )

    organization_memberships: Mapped[
        list["StudentOrganizationMembership"]
    ] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
    )