"""
Verify that all SQLAlchemy ORM models can be configured successfully.
"""

from sqlalchemy.orm import configure_mappers

# Department Domain
import src.models.department
import src.models.department_research_area
import src.models.program
import src.models.research_group

# Lecturer Domain
import src.models.lecturer
import src.models.lecturer_qualification
import src.models.lecturer_expertise
import src.models.lecturer_research_interest
import src.models.lecturer_publication

# Student Domain
import src.models.student
import src.models.student_grade
import src.models.student_course_enrollment
import src.models.disciplinary_record

# Course Domain
import src.models.course
import src.models.course_material
import src.models.course_prerequisite
import src.models.program_course_requirement
import src.models.lecturer_course_teaching

# Staff Domain
import src.models.staff

# Committee Domain
import src.models.committee
import src.models.lecturer_committee_membership

# Student Organization Domain
import src.models.student_organization
import src.models.student_organization_membership

# Research Domain
import src.models.research_project
import src.models.research_project_team
import src.models.research_project_publication


def test_model_configuration() -> None:
    """
    Ensure all SQLAlchemy ORM mappers configure successfully.
    """
    configure_mappers()