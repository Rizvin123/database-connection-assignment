"""
Course Material ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.mixins import ReprMixin

if TYPE_CHECKING:
    from src.models.course import Course


class CourseMaterial(Base, ReprMixin):
    """
    Represents a learning material for a course.
    """

    __tablename__ = "course_materials"

    material_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    course_code: Mapped[str] = mapped_column(
        ForeignKey("courses.course_code"),
        nullable=False,
    )

    material_title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    material_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    material_link: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Relationships

    course: Mapped["Course"] = relationship(
        back_populates="materials"
    )