"""
Dialog for adding and editing courses.
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QSpinBox,
)

from src.models.course import Course
from src.models.department import Department


class CourseDialog(QDialog):
    """
    Dialog used to create or edit a course.
    """

    def __init__(
        self,
        departments: list[Department],
        course: Course | None = None,
    ) -> None:
        super().__init__()

        self._course = course

        self.setWindowTitle(
            "Edit Course"
            if course
            else "Add Course"
        )

        self.setMinimumWidth(500)

        layout = QFormLayout(self)

        #
        # Course Code
        #

        self.course_code_edit = QLineEdit()

        layout.addRow(
            "Course Code",
            self.course_code_edit,
        )

        #
        # Course Name
        #

        self.course_name_edit = QLineEdit()

        layout.addRow(
            "Course Name",
            self.course_name_edit,
        )

        #
        # Description
        #

        self.description_edit = QPlainTextEdit()

        self.description_edit.setFixedHeight(
            100,
        )

        layout.addRow(
            "Description",
            self.description_edit,
        )

        #
        # Department
        #

        self.department_combo = QComboBox()

        for department in departments:

            self.department_combo.addItem(
                department.department_name,
                department.department_id,
            )

        layout.addRow(
            "Department",
            self.department_combo,
        )

        #
        # Level
        #

        self.level_spin = QSpinBox()

        self.level_spin.setRange(
            1,
            10,
        )

        layout.addRow(
            "Level",
            self.level_spin,
        )

        #
        # Credits
        #

        self.credits_spin = QSpinBox()

        self.credits_spin.setRange(
            1,
            60,
        )

        layout.addRow(
            "Credits",
            self.credits_spin,
        )

        #
        # Schedule
        #

        self.schedule_edit = QLineEdit()

        layout.addRow(
            "Schedule",
            self.schedule_edit,
        )

        #
        # Buttons
        #

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(
            self._validate,
        )

        buttons.rejected.connect(
            self.reject,
        )

        layout.addRow(buttons)

        if course:

            self._load_course()

    def _load_course(
        self,
    ) -> None:
        """
        Populate the dialog with an existing course.
        """

        course = self._course

        if course is None:
            return

        self.course_code_edit.setText(
            course.course_code,
        )

        #
        # Course code should not change
        #

        self.course_code_edit.setEnabled(
            False,
        )

        self.course_name_edit.setText(
            course.course_name,
        )

        self.description_edit.setPlainText(
            course.description or "",
        )

        self.level_spin.setValue(
            course.level,
        )

        self.credits_spin.setValue(
            course.credits,
        )

        self.schedule_edit.setText(
            course.schedule or "",
        )

        self._select_combo_data(
            self.department_combo,
            course.department_id,
        )

    @staticmethod
    def _select_combo_data(
        combo: QComboBox,
        value,
    ) -> None:
        """
        Select the combo item whose userData matches.
        """

        for i in range(combo.count()):

            if combo.itemData(i) == value:

                combo.setCurrentIndex(i)

                return

    def _validate(
        self,
    ) -> None:
        """
        Validate required fields.
        """

        if not self.course_code_edit.text().strip():

            QMessageBox.warning(
                self,
                "Validation Error",
                "Course code is required.",
            )

            return

        if not self.course_name_edit.text().strip():

            QMessageBox.warning(
                self,
                "Validation Error",
                "Course name is required.",
            )

            return

        self.accept()

    def get_course_data(
        self,
    ) -> dict:
        """
        Return the entered course data.
        """

        return {
            "course_code": (
                self.course_code_edit.text().strip()
            ),
            "course_name": (
                self.course_name_edit.text().strip()
            ),
            "description": (
                self.description_edit
                .toPlainText()
                .strip()
                or None
            ),
            "department_id": (
                self.department_combo.currentData()
            ),
            "level": (
                self.level_spin.value()
            ),
            "credits": (
                self.credits_spin.value()
            ),
            "schedule": (
                self.schedule_edit.text().strip()
                or None
            ),
        }