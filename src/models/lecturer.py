"""
Lecturer ORM model.
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
    from src.models.department import Department
    from src.models.lecturer_committee_membership import (
        LecturerCommitteeMembership,
    )
    from src.models.lecturer_course_teaching import (
        LecturerCourseTeaching,
    )
    from src.models.lecturer_expertise import LecturerExpertise
    from src.models.lecturer_publication import LecturerPublication
    from src.models.lecturer_qualification import LecturerQualification
    from src.models.lecturer_research_interest import (
        LecturerResearchInterest,
    )
    from src.models.research_group import ResearchGroup
    from src.models.research_project import ResearchProject
    from src.models.research_project_team import (
        ResearchProjectTeam,
    )
    from src.models.student import Student


class Lecturer(Base, ReprMixin):
    """
    Represents a university lecturer.
    """

    __tablename__ = "lecturers"

    lecturer_id: Mapped[int] = mapped_column(
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

    email: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.department_id"),
        nullable=False,
    )

    course_load: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    research_group_id: Mapped[int | None] = mapped_column(
        ForeignKey("research_groups.research_group_id"),
        nullable=True,
    )

    office_room: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    # Relationships

    department: Mapped["Department"] = relationship(
        back_populates="lecturers",
    )

    research_group: Mapped["ResearchGroup | None"] = relationship(
        back_populates="lecturers",
        foreign_keys=[research_group_id],
    )

    qualifications: Mapped[list["LecturerQualification"]] = relationship(
        back_populates="lecturer",
        cascade="all, delete-orphan",
    )

    expertise: Mapped[list["LecturerExpertise"]] = relationship(
        back_populates="lecturer",
        cascade="all, delete-orphan",
    )

    research_interests: Mapped[list["LecturerResearchInterest"]] = relationship(
        back_populates="lecturer",
        cascade="all, delete-orphan",
    )

    publications: Mapped[list["LecturerPublication"]] = relationship(
        back_populates="lecturer",
        cascade="all, delete-orphan",
    )

    advised_students: Mapped[list["Student"]] = relationship(
        back_populates="advisor",
    )

    teaching_assignments: Mapped[list["LecturerCourseTeaching"]] = relationship(
        back_populates="lecturer",
        cascade="all, delete-orphan",
    )

    committee_memberships: Mapped[list["LecturerCommitteeMembership"]] = relationship(
        back_populates="lecturer",
        cascade="all, delete-orphan",
    )

    principal_investigator_projects: Mapped[list["ResearchProject"]] = relationship(
        back_populates="principal_investigator",
        foreign_keys="ResearchProject.principal_investigator_id",
    )

    research_projects: Mapped[list["ResearchProjectTeam"]] = relationship(
        back_populates="lecturer",
        cascade="all, delete-orphan",
    )