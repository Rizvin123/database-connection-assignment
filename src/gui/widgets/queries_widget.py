"""
Widget for executing assignment queries.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.database.session import SessionLocal
from src.gui.models.query_table_model import QueryTableModel
from src.services.query_service import QueryService

class QueriesWidget(QWidget):
    """
    Widget for executing assignment queries.
    """

    def __init__(self) -> None:
        super().__init__()

        #
        # Database
        #

        self._session = SessionLocal()

        self._service = QueryService(
            self._session,
        )

        #
        # User Interface
        #

        self._build_ui()

        self.populate_parameters()

        self.query_combo.currentIndexChanged.connect(
            self.update_parameter_visibility,
        )

        self.run_button.clicked.connect(
            self.run_query,
        )

        self.update_parameter_visibility()

    def _build_ui(self) -> None:
        """
        Build the user interface.
        """

        main_layout = QVBoxLayout(self)

        #
        # Title
        #

        title = QLabel("Queries")

        title.setStyleSheet(
            """
            font-size:22px;
            font-weight:bold;
            """
        )

        main_layout.addWidget(title)

        #
        # Query Selection
        #

        query_group = QGroupBox(
            "Query"
        )

        query_layout = QVBoxLayout(
            query_group
        )

        self.query_combo = QComboBox()

        self.query_combo.addItems(
            [
                "Query 1 - Students by Course and Lecturer",
                "Query 2 - Final-Year Students Above Average",
                "Query 3 - Students Not Enrolled",
                "Query 4 - Faculty Advisor Details",
                "Query 5 - Lecturer Expertise Search",
            ]
        )

        query_layout.addWidget(
            self.query_combo
        )

        main_layout.addWidget(
            query_group
        )

        #
        # Parameters
        #

        parameter_group = QGroupBox(
            "Parameters"
        )

        self.parameter_layout = QVBoxLayout(
            parameter_group
        )

        #
        # Course
        #

        self.course_combo = QComboBox()

        self.course_row = self._add_parameter_row(
            "Course",
            self.course_combo,
        )

        #
        # Lecturer
        #

        self.lecturer_combo = QComboBox()

        self.lecturer_row = self._add_parameter_row(
            "Lecturer",
            self.lecturer_combo,
        )

        #
        # Semester
        #

        self.semester_combo = QComboBox()

        self.semester_row = self._add_parameter_row(
            "Semester",
            self.semester_combo,
        )

        main_layout.addWidget(
            parameter_group
        )

        #
        # Academic Year
        #

        self.academic_year_combo = QComboBox()

        self.academic_year_row = self._add_parameter_row(
            "Academic Year",
            self.academic_year_combo,
        )

        #
        # Average Threshold
        #

        self.average_spin = QSpinBox()

        self.average_spin.setRange(
            0,
            100,
        )

        self.average_spin.setValue(
            70,
        )

        self.average_row = self._add_parameter_row(
            "Average Threshold",
            self.average_spin,
        )

        #
        # Student
        #

        self.student_combo = QComboBox()

        self.student_row = self._add_parameter_row(
            "Student",
            self.student_combo,
        )

        #
        # Research Area
        #

        self.research_area_combo = QComboBox()

        self.research_area_row = self._add_parameter_row(
            "Research Area",
            self.research_area_combo,
        )

        #
        # Run Query Button
        #

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        self.run_button = QPushButton(
            "Run Query"
        )

        button_layout.addWidget(
            self.run_button
        )

        main_layout.addLayout(
            button_layout
        )

        #
        # Results Table
        #

        self.table = QTableView()

        self.model = QueryTableModel()

        self.table.setModel(
            self.model
        )

        self.table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableView.SelectionMode.SingleSelection
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.horizontalHeader().setStretchLastSection(
            True
        )

        self.table.verticalHeader().setVisible(
            False
        )

        main_layout.addWidget(
            self.table
        )

        #
        # Status
        #

        self.status_label = QLabel(
            "0 result(s)"
        )

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        main_layout.addWidget(
            self.status_label
        )
    def closeEvent(
        self,
        event,
    ) -> None:
        """
        Close the database session.
        """

        self._session.close()

        super().closeEvent(event)

    def _add_parameter_row(
        self,
        label_text: str,
        widget: QWidget,
    ) -> QWidget:
        """
        Create a labelled parameter row.
        """

        row = QWidget()

        layout = QHBoxLayout(row)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        label = QLabel(
            label_text,
        )

        label.setMinimumWidth(
            150,
        )

        layout.addWidget(
            label,
        )

        layout.addWidget(
            widget,
            1,
        )

        self.parameter_layout.addWidget(
            row,
        )

        return row
    
    def populate_parameters(self) -> None:
        """
        Populate all parameter controls.
        """

        #
        # Courses
        #

        self.course_combo.clear()

        for course in self._service.get_courses():

            self.course_combo.addItem(
                f"{course.course_code} - "
                f"{course.course_name}",
                course.course_code,
            )

        #
        # Lecturers
        #

        self.lecturer_combo.clear()

        for lecturer in self._service.get_lecturers():

            self.lecturer_combo.addItem(
                f"{lecturer.first_name} "
                f"{lecturer.last_name}",
                lecturer.lecturer_id,
            )

        #
        # Students
        #

        self.student_combo.clear()

        for student in self._service.get_students():

            self.student_combo.addItem(
                f"{student.first_name} "
                f"{student.last_name}",
                student.student_id,
            )

        #
        # Semesters
        #

        self.semester_combo.clear()

        for semester in self._service.get_semesters():

            self.semester_combo.addItem(
                semester,
            )

        #
        # Academic Years
        #

        self.academic_year_combo.clear()

        for year in self._service.get_academic_years():

            self.academic_year_combo.addItem(
                year,
            )

        #
        # Research Areas
        #

        self.research_area_combo.clear()

        for area in self._service.get_research_areas():

            self.research_area_combo.addItem(
                area,
            )

    def update_parameter_visibility(self) -> None:
        """
        Show only the parameters required for the
        selected query.
        """

        #
        # Hide all parameter rows
        #

        self.course_row.hide()

        self.lecturer_row.hide()

        self.semester_row.hide()

        self.academic_year_row.hide()

        self.average_row.hide()

        self.student_row.hide()

        self.research_area_row.hide()

        index = self.query_combo.currentIndex()

        #
        # Query 1
        #

        if index == 0:

            self.course_row.show()

            self.lecturer_row.show()

            self.semester_row.show()

            self.academic_year_row.show()

        #
        # Query 2
        #

        elif index == 1:

            self.average_row.show()

        #
        # Query 3
        #

        elif index == 2:

            self.semester_row.show()

            self.academic_year_row.show()

        #
        # Query 4
        #

        elif index == 3:

            self.student_row.show()

        #
        # Query 5
        #

        elif index == 4:

            self.research_area_row.show()

    def run_query(self) -> None:
        """
        Execute the selected query.
        """

        index = self.query_combo.currentIndex()

        #
        # Query 1
        #

        if index == 0:

            results = (
                self._service.students_by_course_and_lecturer(
                    course_code=self.course_combo.currentData(),
                    lecturer_id=self.lecturer_combo.currentData(),
                    semester=self.semester_combo.currentText(),
                    academic_year=self.academic_year_combo.currentText(),
                )
            )

            headers = [
                "Student ID",
                "First Name",
                "Last Name",
                "Course Code",
                "Course Name",
                "Lecturer",
            ]

            rows = []

            for student, course, lecturer in results:

                rows.append(
                    [
                        student.student_id,
                        student.first_name,
                        student.last_name,
                        course.course_code,
                        course.course_name,
                        f"{lecturer.first_name} {lecturer.last_name}",
                    ]
                )

            self.model.set_results(
                headers,
                rows,
            )

            self.status_label.setText(
                f"{len(rows)} result(s)"
            )

        #
        # Query 2
        #

        elif index == 1:

            results = (
                self._service.final_year_students_above_average(
                    minimum_average=self.average_spin.value(),
                )
            )

            headers = [
                "Student ID",
                "First Name",
                "Last Name",
                "Programme",
                "Year",
                "Average Grade",
            ]

            rows = []

            for student, program, average_grade in results:

                rows.append(
                    [
                        student.student_id,
                        student.first_name,
                        student.last_name,
                        program.program_name,
                        student.year_of_study,
                        float(average_grade),
                    ]
                )

            self.model.set_results(
                headers,
                rows,
            )

            self.status_label.setText(
                f"{len(rows)} result(s)"
            )

        #
        # Query 3
        #

        elif index == 2:

            results = (
                self._service.students_not_enrolled(
                    semester=self.semester_combo.currentText(),
                    academic_year=self.academic_year_combo.currentText(),
                )
            )

            headers = [
                "Student ID",
                "First Name",
                "Last Name",
                "Email",
            ]

            rows = []

            for student in results:

                rows.append(
                    [
                        student.student_id,
                        student.first_name,
                        student.last_name,
                        student.email,
                    ]
                )

            self.model.set_results(
                headers,
                rows,
            )

            self.status_label.setText(
                f"{len(rows)} result(s)"
            )

        #
        # Query 4
        #

        elif index == 3:

            result = (
                self._service.faculty_advisor_details(
                    student_id=self.student_combo.currentData(),
                )
            )

            headers = [
                "Student ID",
                "Student",
                "Advisor ID",
                "Advisor",
                "Email",
                "Phone",
                "Office",
            ]

            rows = []

            if result is not None:

                student, advisor = result

                rows.append(
                    [
                        student.student_id,
                        f"{student.first_name} {student.last_name}",
                        advisor.lecturer_id if advisor else "",
                        (
                            f"{advisor.first_name} {advisor.last_name}"
                            if advisor
                            else "Not Assigned"
                        ),
                        advisor.email if advisor else "",
                        advisor.phone if advisor else "",
                        advisor.office_room if advisor else "",
                    ]
                )

            self.model.set_results(
                headers,
                rows,
            )

            self.status_label.setText(
                f"{len(rows)} result(s)"
            )

        #
        # Query 5
        #

        elif index == 4:

            results = (
                self._service.lecturers_by_research_area(
                    research_area=self.research_area_combo.currentText(),
                )
            )

            headers = [
                "Lecturer ID",
                "First Name",
                "Last Name",
                "Email",
                "Expertise Area",
            ]

            rows = []

            for lecturer, expertise in results:

                rows.append(
                    [
                        lecturer.lecturer_id,
                        lecturer.first_name,
                        lecturer.last_name,
                        lecturer.email,
                        expertise.expertise_area,
                    ]
                )

            self.model.set_results(
                headers,
                rows,
            )

            self.status_label.setText(
                f"{len(rows)} result(s)"
            )