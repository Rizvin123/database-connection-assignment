"""
Dialog for adding and editing students.
"""

from __future__ import annotations

from datetime import date

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QSpinBox,
)

from src.models.lecturer import Lecturer
from src.models.program import Program
from src.models.student import Student


class StudentDialog(QDialog):
    """
    Dialog used to create or edit a student.
    """

    def __init__(
        self,
        programs: list[Program],
        advisors: list[Lecturer],
        student: Student | None = None,
    ) -> None:
        super().__init__()

        self._student = student

        self.setWindowTitle(
            "Edit Student"
            if student
            else "Add Student"
        )

        self.setMinimumWidth(500)

        layout = QFormLayout(self)

        # First Name

        self.first_name_edit = QLineEdit()

        layout.addRow(
            "First Name",
            self.first_name_edit,
        )

        # Last Name

        self.last_name_edit = QLineEdit()

        layout.addRow(
            "Last Name",
            self.last_name_edit,
        )

        # Date of Birth

        self.date_of_birth_edit = QDateEdit()

        self.date_of_birth_edit.setCalendarPopup(True)

        self.date_of_birth_edit.setDate(
            QDate.currentDate()
        )

        layout.addRow(
            "Date of Birth",
            self.date_of_birth_edit,
        )

        # Email

        self.email_edit = QLineEdit()

        layout.addRow(
            "Email",
            self.email_edit,
        )

        # Phone

        self.phone_edit = QLineEdit()

        layout.addRow(
            "Phone",
            self.phone_edit,
        )

        # Address

        self.address_edit = QLineEdit()

        layout.addRow(
            "Address",
            self.address_edit,
        )

        # Program

        self.program_combo = QComboBox()

        for program in programs:
            self.program_combo.addItem(
                program.program_name,
                program.program_id,
            )

        layout.addRow(
            "Program",
            self.program_combo,
        )

        # Year

        self.year_spin = QSpinBox()

        self.year_spin.setMinimum(1)

        self.year_spin.setMaximum(10)

        layout.addRow(
            "Year of Study",
            self.year_spin,
        )

        # Advisor

        self.advisor_combo = QComboBox()

        self.advisor_combo.addItem(
            "None",
            None,
        )

        for lecturer in advisors:
            self.advisor_combo.addItem(
                f"{lecturer.first_name} {lecturer.last_name}",
                lecturer.lecturer_id,
            )

        layout.addRow(
            "Advisor",
            self.advisor_combo,
        )

        # Graduation Status

        self.status_combo = QComboBox()

        self.status_combo.addItems(
            [
                "Not Graduated",
                "Graduated",
            ]
        )

        layout.addRow(
            "Graduation Status",
            self.status_combo,
        )

        # Buttons

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(
            self._validate
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addRow(buttons)

        if student:
            self._load_student()

    def _load_student(
        self,
    ) -> None:
        """
        Populate the dialog with an existing student's data.
        """

        student = self._student

        if student is None:
            return

        self.first_name_edit.setText(
            student.first_name
        )

        self.last_name_edit.setText(
            student.last_name
        )

        if student.date_of_birth:
            self.date_of_birth_edit.setDate(
                QDate(
                    student.date_of_birth.year,
                    student.date_of_birth.month,
                    student.date_of_birth.day,
                )
            )

        self.email_edit.setText(
            student.email
        )

        self.phone_edit.setText(
            student.phone or ""
        )

        self.address_edit.setText(
            student.address or ""
        )

        self.year_spin.setValue(
            student.year_of_study
        )

        self.status_combo.setCurrentText(
            student.graduation_status
        )

        self._select_combo_data(
            self.program_combo,
            student.program_id,
        )

        self._select_combo_data(
            self.advisor_combo,
            student.advisor_lecturer_id,
        )

    @staticmethod
    def _select_combo_data(
        combo: QComboBox,
        value,
    ) -> None:
        """
        Select the combo box item whose userData matches value.
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

        if not self.first_name_edit.text().strip():
            QMessageBox.warning(
                self,
                "Validation Error",
                "First name is required.",
            )
            return

        if not self.last_name_edit.text().strip():
            QMessageBox.warning(
                self,
                "Validation Error",
                "Last name is required.",
            )
            return

        if not self.email_edit.text().strip():
            QMessageBox.warning(
                self,
                "Validation Error",
                "Email is required.",
            )
            return

        self.accept()

    def get_student_data(
        self,
    ) -> dict:
        """
        Return the entered student data.
        """

        qdate = self.date_of_birth_edit.date()

        return {
            "first_name": self.first_name_edit.text().strip(),
            "last_name": self.last_name_edit.text().strip(),
            "date_of_birth": date(
                qdate.year(),
                qdate.month(),
                qdate.day(),
            ),
            "email": self.email_edit.text().strip(),
            "phone": self.phone_edit.text().strip() or None,
            "address": self.address_edit.text().strip() or None,
            "program_id": self.program_combo.currentData(),
            "year_of_study": self.year_spin.value(),
            "advisor_lecturer_id": self.advisor_combo.currentData(),
            "graduation_status": self.status_combo.currentText(),
        }