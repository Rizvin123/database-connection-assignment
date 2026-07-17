"""
Course Prerequisite ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.course import Course


class CoursePrerequisite(Base, ReprMixin):
    """
    Represents a prerequisite relationship between two courses.
    """

    __tablename__ = "course_prerequisites"

    course_code: Mapped[str] = mapped_column(
        ForeignKey("courses.course_code"),
        primary_key=True,
    )

    prerequisite_course_code: Mapped[str] = mapped_column(
        ForeignKey("courses.course_code"),
        primary_key=True,
    )

    # Relationships

    course: Mapped["Course"] = relationship(
        foreign_keys=[course_code],
        back_populates="prerequisites",
    )

    prerequisite_course: Mapped["Course"] = relationship(
        foreign_keys=[prerequisite_course_code],
        back_populates="prerequisite_for",
    )