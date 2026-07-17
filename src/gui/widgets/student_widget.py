"""
Student management widget.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from PyQt6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QComboBox,
)

from PyQt6.QtWidgets import QMessageBox

from src.gui.dialogs.student_dialog import StudentDialog
from src.models.student import Student

from src.repositories.program_repository import ProgramRepository
from src.repositories.lecturer_repository import LecturerRepository

from src.database.session import SessionLocal
from src.gui.models.student_table_model import StudentTableModel
from src.repositories.student_repository import StudentRepository
from src.services.student_service import StudentService


class StudentWidget(QWidget):
    """
    Widget for displaying and managing students.
    """

    def __init__(self) -> None:
        super().__init__()

        # Database layer

        self._session = SessionLocal()

        self._student_repository = StudentRepository(self._session)
        self._service = StudentService(self._student_repository)

        self._program_repository = ProgramRepository(self._session)
        self._lecturer_repository = LecturerRepository(self._session)

        # UI

        self._build_ui()

        self.load_students()

        self.load_filters()

    def _build_ui(self) -> None:
        """
        Create the user interface.
        """

        main_layout = QVBoxLayout(self)

        title = QLabel("Students")
        title.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            """
        )

        main_layout.addWidget(title)

        search_group = QGroupBox("Search & Filters")

        search_layout = QFormLayout(search_group)

        self.search_field_combo = QComboBox()

        self.search_field_combo.addItem(
            "First Name",
            "first_name",
        )

        self.search_field_combo.addItem(
            "Last Name",
            "last_name",
        )

        self.search_field_combo.addItem(
            "Email",
            "email",
        )

        self.search_edit = QLineEdit()

        self.program_filter = QComboBox()

        self.year_filter = QComboBox()

        self.status_filter = QComboBox()

        self.clear_button = QPushButton("Clear")

        search_layout.addRow(
            "Search By",
            self.search_field_combo,
        )

        search_layout.addRow(
            "Search",
            self.search_edit,
        )

        search_layout.addRow(
            "Program",
            self.program_filter,
        )

        search_layout.addRow(
            "Year",
            self.year_filter,
        )

        search_layout.addRow(
            "Graduation Status",
            self.status_filter,
        )

        search_layout.addRow(
            "",
            self.clear_button,
        )

        main_layout.addWidget(search_group)

        # Table

        self.table = QTableView()

        self.model = StudentTableModel()

        self.table.setModel(self.model)

        self.table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableView.SelectionMode.SingleSelection
        )

        self.table.setAlternatingRowColors(True)

        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.verticalHeader().setVisible(False)

        main_layout.addWidget(self.table)

        # Buttons

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add")

        self.edit_button = QPushButton("Edit")

        self.delete_button = QPushButton("Delete")

        self.refresh_button = QPushButton("Refresh")

        button_layout.addWidget(self.add_button)

        button_layout.addWidget(self.edit_button)

        button_layout.addWidget(self.delete_button)

        button_layout.addStretch()

        button_layout.addWidget(self.refresh_button)

        main_layout.addLayout(button_layout)

        # Status

        self.status_label = QLabel()

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        main_layout.addWidget(self.status_label)

        # Signals

        self.refresh_button.clicked.connect(
            self.load_students,
        )

        self.clear_button.clicked.connect(
            self.clear_filters,
        )

        self.search_edit.returnPressed.connect(
            self.search_students,
        )

        self.search_field_combo.currentIndexChanged.connect(
            self.search_students,
        )

        self.program_filter.currentIndexChanged.connect(
            self.search_students,
        )

        self.year_filter.currentIndexChanged.connect(
            self.search_students,
        )

        self.status_filter.currentIndexChanged.connect(
            self.search_students,
        )

        self.add_button.clicked.connect(
            self.add_student
        )

        self.edit_button.clicked.connect(
            self.edit_student
        )

        self.delete_button.clicked.connect(
            self.delete_student
        )

    def load_students(self) -> None:
        """
        Load students from the database.
        """

        students = self._service.get_all_students()

        self.model.set_students(students)

        self.status_label.setText(
            f"{len(students)} student(s)"
        )

    def closeEvent(self, event) -> None:
        """
        Close the database session.
        """

        self._session.close()

        super().closeEvent(event)

    def add_student(self) -> None:
        """
        Open the Add Student dialog.
        """

        programs = self._program_repository.get_program_names()

        advisors = self._lecturer_repository.get_advisors()

        dialog = StudentDialog(
            programs=programs,
            advisors=advisors,
        )

        if dialog.exec():

            data = dialog.get_student_data()

            student = Student(**data)

            try:

                self._service.create_student(student)

            except ValueError as exc:

                QMessageBox.warning(
                    self,
                    "Unable to Create Student",
                    str(exc),
                )

                return

            self.load_students()

            QMessageBox.information(
                self,
                "Success",
                "Student added successfully.",
            )

    def selected_student(self) -> Student | None:
        """
        Return the currently selected student.
        """

        selection = self.table.selectionModel().selectedRows()

        if not selection:
            return None

        row = selection[0].row()

        return self.model.student_at(row)
    
    def edit_student(self) -> None:
        """
        Edit the selected student.
        """

        student = self.selected_student()

        if student is None:

            QMessageBox.information(
                self,
                "Edit Student",
                "Please select a student.",
            )

            return

        programs = self._program_repository.get_program_names()

        advisors = self._lecturer_repository.get_advisors()

        dialog = StudentDialog(
            programs=programs,
            advisors=advisors,
            student=student,
        )

        if not dialog.exec():
            return

        data = dialog.get_student_data()

        student.first_name = data["first_name"]
        student.last_name = data["last_name"]
        student.date_of_birth = data["date_of_birth"]
        student.email = data["email"]
        student.phone = data["phone"]
        student.address = data["address"]
        student.program_id = data["program_id"]
        student.year_of_study = data["year_of_study"]
        student.advisor_lecturer_id = data["advisor_lecturer_id"]
        student.graduation_status = data["graduation_status"]

        try:

            self._service.update_student()

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Update Failed",
                str(exc),
            )

            return

        self.load_students()

        QMessageBox.information(
            self,
            "Success",
            "Student updated successfully.",
        )

    def delete_student(self) -> None:
        """
        Delete the selected student.
        """

        student = self.selected_student()

        if student is None:

            QMessageBox.information(
                self,
                "Delete Student",
                "Please select a student.",
            )

            return

        answer = QMessageBox.question(
            self,
            "Delete Student",
            (
                f"Delete {student.first_name} "
                f"{student.last_name}?"
            ),
            QMessageBox.StandardButton.Yes
            |
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:

            self._service.delete_student(
                student.student_id,
            )

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Delete Failed",
                str(exc),
            )

            return

        self.load_students()

        QMessageBox.information(
            self,
            "Success",
            "Student deleted successfully.",
        )
    
    def load_filters(self) -> None:
        """
        Populate filter combo boxes.
        """

        self.program_filter.clear()

        self.program_filter.addItem(
            "All Programs",
            None,
        )

        for program in self._program_repository.get_program_names():

            self.program_filter.addItem(
                program.program_name,
                program.program_id,
            )

        self.year_filter.clear()

        self.year_filter.addItem(
            "All Years",
            None,
        )

        for year in range(1, 11):

            self.year_filter.addItem(
                str(year),
                year,
            )

        self.status_filter.clear()

        self.status_filter.addItem(
            "All",
            None,
        )

        self.status_filter.addItem(
            "Not Graduated",
            "Not Graduated",
        )

        self.status_filter.addItem(
            "Graduated",
            "Graduated",
        )

    def search_students(self, *args) -> None:
        """
        Search students.
        """

        students = self._service.search_students(
            search_field=self.search_field_combo.currentData(),
            search_text=self.search_edit.text(),
            program_id=self.program_filter.currentData(),
            year_of_study=self.year_filter.currentData(),
            graduation_status=self.status_filter.currentData(),
        )

        self.model.set_students(students)

        self.status_label.setText(
            f"{len(students)} student(s)"
        )
    
    def clear_filters(self) -> None:
        """
        Reset every search control.
        """

        self.search_field_combo.blockSignals(True)
        self.program_filter.blockSignals(True)
        self.year_filter.blockSignals(True)
        self.status_filter.blockSignals(True)

        self.search_field_combo.setCurrentIndex(0)
        self.search_edit.clear()
        self.program_filter.setCurrentIndex(0)
        self.year_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)

        self.search_field_combo.blockSignals(False)
        self.program_filter.blockSignals(False)
        self.year_filter.blockSignals(False)
        self.status_filter.blockSignals(False)

        self.load_students()