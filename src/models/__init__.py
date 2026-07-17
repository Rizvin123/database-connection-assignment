"""
Import all ORM models.

Importing this package registers every SQLAlchemy mapper so that
relationships can be resolved correctly throughout the application.
"""

# Department Domain
from src.models.department import Department
from src.models.department_research_area import DepartmentResearchArea

# Program Domain
from src.models.program import Program

# Research Group Domain
from src.models.research_group import ResearchGroup

# Lecturer Domain
from src.models.lecturer import Lecturer
from src.models.lecturer_qualification import LecturerQualification
from src.models.lecturer_expertise import LecturerExpertise
from src.models.lecturer_research_interest import LecturerResearchInterest
from src.models.lecturer_publication import LecturerPublication

# Student Domain
from src.models.student import Student
from src.models.student_grade import StudentGrade
from src.models.student_course_enrollment import StudentCourseEnrollment
from src.models.disciplinary_record import DisciplinaryRecord

# Course Domain
from src.models.course import Course
from src.models.course_material import CourseMaterial
from src.models.course_prerequisite import CoursePrerequisite
from src.models.program_course_requirement import ProgramCourseRequirement
from src.models.lecturer_course_teaching import LecturerCourseTeaching

# Staff Domain
from src.models.staff import Staff

# Committee Domain
from src.models.committee import Committee
from src.models.lecturer_committee_membership import (
    LecturerCommitteeMembership,
)

# Student Organization Domain
from src.models.student_organization import StudentOrganization
from src.models.student_organization_membership import (
    StudentOrganizationMembership,
)

# Research Domain
from src.models.research_project import ResearchProject
from src.models.research_project_team import ResearchProjectTeam
from src.models.research_project_publication import (
    ResearchProjectPublication,
)