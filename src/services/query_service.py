"""
Service layer for assignment queries.
"""
from __future__ import annotations

from sqlalchemy import func
from sqlalchemy import exists
from sqlalchemy import distinct

from sqlalchemy.orm import Session

from src.models.course import Course
from src.models.lecturer import Lecturer
from src.models.lecturer_course_teaching import (
    LecturerCourseTeaching,
)
from src.models.student import Student
from src.models.student_course_enrollment import (
    StudentCourseEnrollment,
)

from src.models.program import Program
from src.models.student_grade import StudentGrade
from src.models.lecturer_expertise import LecturerExpertise



class QueryService:
    """
    Executes read-only reporting queries.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        """
        Initialise the query service.
        """

        self._session = session

    def students_by_course_and_lecturer(
    self,
    course_code: str,
    lecturer_id: int,
    semester: str,
    academic_year: str,
    ) -> list[tuple[Student, Course, Lecturer]]:
        """
        Return students enrolled in a selected course
        taught by the selected lecturer during the
        specified semester and academic year.
        """

        return (
            self._session.query(
                Student,
                Course,
                Lecturer,
            )
            .join(
                StudentCourseEnrollment,
                Student.student_id
                == StudentCourseEnrollment.student_id,
            )
            .join(
                Course,
                StudentCourseEnrollment.course_code
                == Course.course_code,
            )
            .join(
                LecturerCourseTeaching,
                (
                    StudentCourseEnrollment.course_code
                    == LecturerCourseTeaching.course_code
                )
                &
                (
                    StudentCourseEnrollment.semester
                    == LecturerCourseTeaching.semester
                )
                &
                (
                    StudentCourseEnrollment.academic_year
                    == LecturerCourseTeaching.academic_year
                ),
            )
            .join(
                Lecturer,
                LecturerCourseTeaching.lecturer_id
                == Lecturer.lecturer_id,
            )
            .filter(
                StudentCourseEnrollment.course_code
                == course_code,
                Lecturer.lecturer_id
                == lecturer_id,
                StudentCourseEnrollment.semester
                == semester,
                StudentCourseEnrollment.academic_year
                == academic_year,
            )
            .order_by(
                Student.last_name,
                Student.first_name,
            )
            .all()
        )
    
    def final_year_students_above_average(
    self,
    minimum_average: float,
    ) -> list[tuple[Student, Program, float]]:
        """
        Return final-year students whose average
        assessment score exceeds the supplied
        threshold.
        """

        return (
            self._session.query(
                Student,
                Program,
                func.round(
                    func.avg(
                        StudentGrade.score,
                    ),
                    2,
                ).label(
                    "average_grade",
                ),
            )
            .join(
                Program,
                Student.program_id
                == Program.program_id,
            )
            .join(
                StudentGrade,
                Student.student_id
                == StudentGrade.student_id,
            )
            .filter(
                Student.year_of_study
                == Program.duration_years,
            )
            .group_by(
                Student.student_id,
                Student.first_name,
                Student.last_name,
                Student.year_of_study,
                Program.program_id,
                Program.program_name,
            )
            .having(
                func.avg(
                    StudentGrade.score,
                )
                > minimum_average,
            )
            .order_by(
                func.avg(
                    StudentGrade.score,
                ).desc(),
            )
            .all()
        )
    
    def students_not_enrolled(
    self,
    semester: str,
    academic_year: str,
    ) -> list[Student]:
        """
        Return students who have not registered for
        any course during the specified semester
        and academic year.
        """

        enrollment_exists = (
            self._session.query(
                StudentCourseEnrollment.student_id,
            )
            .filter(
                StudentCourseEnrollment.student_id
                == Student.student_id,
                StudentCourseEnrollment.semester
                == semester,
                StudentCourseEnrollment.academic_year
                == academic_year,
            )
            .exists()
        )

        return (
            self._session.query(
                Student,
            )
            .filter(
                ~enrollment_exists,
            )
            .order_by(
                Student.last_name,
                Student.first_name,
            )
            .all()
        )
    
    def faculty_advisor_details(
    self,
    student_id: int,
    ) -> tuple[Student, Lecturer | None] | None:
        """
        Return the faculty advisor details for the
        specified student.

        Returns a tuple containing the Student and
        the assigned Lecturer. If the student has
        no advisor, the Lecturer element will be None.
        """

        student = (
            self._session.query(
                Student,
            )
            .filter(
                Student.student_id == student_id,
            )
            .first()
        )

        if student is None:

            return None

        return (
            student,
            student.advisor,
        )
    
    def lecturers_by_research_area(
    self,
    research_area: str,
    ) -> list[tuple[Lecturer, LecturerExpertise]]:
        """
        Return lecturers whose expertise contains
        the supplied research area.
        """

        return (
            self._session.query(
                Lecturer,
                LecturerExpertise,
            )
            .join(
                LecturerExpertise,
                Lecturer.lecturer_id
                == LecturerExpertise.lecturer_id,
            )
            .filter(
                LecturerExpertise.expertise_area.ilike(
                    f"%{research_area}%"
                )
            )
            .order_by(
                Lecturer.last_name,
                Lecturer.first_name,
            )
            .all()
        )
    
    def get_courses(
    self,
    ) -> list[Course]:
        """
        Return all courses ordered by course code.
        """

        return (
            self._session.query(
                Course,
            )
            .order_by(
                Course.course_code,
            )
            .all()
        )
    
    def get_lecturers(
    self,
    ) -> list[Lecturer]:
        """
        Return all lecturers.
        """

        return (
            self._session.query(
                Lecturer,
            )
            .order_by(
                Lecturer.last_name,
                Lecturer.first_name,
            )
            .all()
        )
    
    def get_students(
    self,
    ) -> list[Student]:
        """
        Return all students.
        """

        return (
            self._session.query(
                Student,
            )
            .order_by(
                Student.last_name,
                Student.first_name,
            )
            .all()
        )
    
    def get_semesters(
    self,
    ) -> list[str]:
        """
        Return all semesters.
        """

        return [

            semester

            for (
                semester,
            ) in (

                self._session.query(

                    distinct(
                        StudentCourseEnrollment.semester,
                    )

                )

                .order_by(
                    StudentCourseEnrollment.semester,
                )

                .all()

            )

        ]
    
    def get_academic_years(
    self,
    ) -> list[str]:
        """
        Return all academic years.
        """

        return [

            year

            for (
                year,
            ) in (

                self._session.query(

                    distinct(
                        StudentCourseEnrollment.academic_year,
                    )

                )

                .order_by(
                    StudentCourseEnrollment.academic_year.desc(),
                )

                .all()

            )

        ]
    
    def get_research_areas(
    self,
    ) -> list[str]:
        """
        Return all research areas.
        """

        return [

            area

            for (
                area,
            ) in (

                self._session.query(

                    distinct(
                        LecturerExpertise.expertise_area,
                    )

                )

                .order_by(
                    LecturerExpertise.expertise_area,
                )

                .all()

            )

        ]