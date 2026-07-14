"""
Course management widget.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from PyQt6.QtWidgets import QMessageBox

from src.gui.dialogs.course_dialog import CourseDialog
from src.models.course import Course

from src.database.session import SessionLocal
from src.gui.models.course_table_model import CourseTableModel
from src.repositories.course_repository import CourseRepository
from src.repositories.department_repository import DepartmentRepository
from src.services.course_service import CourseService


class CourseWidget(QWidget):
    """
    Widget for displaying and managing courses.
    """

    def __init__(self) -> None:
        super().__init__()

        #
        # Database layer
        #

        self._session = SessionLocal()

        self._course_repository = CourseRepository(
            self._session,
        )

        self._department_repository = DepartmentRepository(
            self._session,
        )

        self._service = CourseService(
            self._session,
        )

        #
        # UI
        #

        self._build_ui()

        self.load_courses()

        self.load_filters()

    def _build_ui(
        self,
    ) -> None:
        """
        Build the user interface.
        """

        main_layout = QVBoxLayout(self)

        #
        # Title
        #

        title = QLabel("Courses")

        title.setStyleSheet(
            """
            font-size:22px;
            font-weight:bold;
            """
        )

        main_layout.addWidget(title)

        #
        # Search
        #

        search_group = QGroupBox(
            "Search & Filters"
        )

        search_layout = QFormLayout(search_group)

        self.search_field_combo = QComboBox()

        self.search_field_combo.addItem(
            "Course Code",
            "course_code",
        )

        self.search_field_combo.addItem(
            "Course Name",
            "course_name",
        )

        self.search_edit = QLineEdit()

        self.department_filter = QComboBox()

        self.level_filter = QComboBox()

        self.clear_button = QPushButton(
            "Clear"
        )

        search_layout.addRow(
            "Search By",
            self.search_field_combo,
        )

        search_layout.addRow(
            "Search",
            self.search_edit,
        )

        search_layout.addRow(
            "Department",
            self.department_filter,
        )

        search_layout.addRow(
            "Level",
            self.level_filter,
        )

        search_layout.addRow(
            "",
            self.clear_button,
        )

        main_layout.addWidget(
            search_group,
        )

        #
        # Table
        #

        self.table = QTableView()

        self.model = CourseTableModel()

        self.table.setModel(
            self.model,
        )

        self.table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows,
        )

        self.table.setSelectionMode(
            QTableView.SelectionMode.SingleSelection,
        )

        self.table.setAlternatingRowColors(
            True,
        )

        self.table.horizontalHeader().setStretchLastSection(
            True,
        )

        self.table.verticalHeader().setVisible(
            False,
        )

        main_layout.addWidget(
            self.table,
        )

        #
        # Buttons
        #

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add")
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")
        self.refresh_button = QPushButton("Refresh")

        button_layout.addWidget(
            self.add_button,
        )

        button_layout.addWidget(
            self.edit_button,
        )

        button_layout.addWidget(
            self.delete_button,
        )

        button_layout.addStretch()

        button_layout.addWidget(
            self.refresh_button,
        )

        main_layout.addLayout(
            button_layout,
        )

        #
        # Status
        #

        self.status_label = QLabel()

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft,
        )

        main_layout.addWidget(
            self.status_label,
        )

        #
        # Signals
        #

        self.refresh_button.clicked.connect(
            self.load_courses,
        )

        self.add_button.clicked.connect(
            self.add_course,
        )

        self.edit_button.clicked.connect(
            self.edit_course,
        )

        self.delete_button.clicked.connect(
            self.delete_course,
        )

    def load_courses(
        self,
    ) -> None:
        """
        Load courses from the database.
        """

        courses = self._service.get_all_courses()

        self.model.set_courses(
            courses,
        )

        self.status_label.setText(
            f"{len(courses)} course(s)"
        )

    def load_filters(
        self,
    ) -> None:
        """
        Populate filter controls.
        """

        self.department_filter.clear()

        self.department_filter.addItem(
            "All Departments",
            None,
        )

        for department in (
            self._department_repository.get_department_names()
        ):

            self.department_filter.addItem(
                department.department_name,
                department.department_id,
            )

        self.level_filter.clear()

        self.level_filter.addItem(
            "All Levels",
            None,
        )

        for level in range(1, 11):

            self.level_filter.addItem(
                str(level),
                level,
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

    def selected_course(self) -> Course | None:
        """
        Return the selected course.
        """

        selection = (
            self.table.selectionModel()
            .selectedRows()
        )

        if not selection:
            return None

        return self.model.course_at(
            selection[0].row()
        )
    
    def add_course(self) -> None:
        """
        Add a new course.
        """

        departments = (
            self._department_repository.get_department_names()
        )

        dialog = CourseDialog(
            departments=departments,
        )

        if not dialog.exec():
            return

        data = dialog.get_course_data()

        course = Course(**data)

        try:

            self._service.create_course(
                course,
            )

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Unable to Create Course",
                str(exc),
            )

            return

        self.load_courses()

        QMessageBox.information(
            self,
            "Success",
            "Course added successfully.",
        )
    
    def edit_course(self) -> None:
        """
        Edit the selected course.
        """

        course = self.selected_course()

        if course is None:

            QMessageBox.information(
                self,
                "Edit Course",
                "Please select a course.",
            )

            return

        departments = (
            self._department_repository.get_department_names()
        )

        dialog = CourseDialog(
            departments=departments,
            course=course,
        )

        if not dialog.exec():
            return

        data = dialog.get_course_data()

        #
        # Primary key is not editable
        #

        course.course_name = data["course_name"]
        course.description = data["description"]
        course.department_id = data["department_id"]
        course.level = data["level"]
        course.credits = data["credits"]
        course.schedule = data["schedule"]

        try:

            self._service.update_course()

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Update Failed",
                str(exc),
            )

            return

        self.load_courses()

        QMessageBox.information(
            self,
            "Success",
            "Course updated successfully.",
        )

    def delete_course(self) -> None:
        """
        Delete the selected course.
        """

        course = self.selected_course()

        if course is None:

            QMessageBox.information(
                self,
                "Delete Course",
                "Please select a course.",
            )

            return

        answer = QMessageBox.question(
            self,
            "Delete Course",
            (
                f"Delete "
                f"{course.course_code} - "
                f"{course.course_name}?"
            ),
            QMessageBox.StandardButton.Yes
            |
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:

            self._service.delete_course(
                course.course_code,
            )

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Delete Failed",
                str(exc),
            )

            return

        self.load_courses()

        QMessageBox.information(
            self,
            "Success",
            "Course deleted successfully.",
        )