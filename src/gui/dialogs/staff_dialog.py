"""
Dialog for adding and editing staff members.
"""

from __future__ import annotations

from decimal import Decimal

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
)

from src.models.department import Department
from src.models.staff import Staff


class StaffDialog(QDialog):
    """
    Dialog used to create or edit a staff member.
    """

    def __init__(
        self,
        departments: list[Department],
        staff: Staff | None = None,
    ) -> None:
        super().__init__()

        self._staff = staff

        self.setWindowTitle(
            "Edit Staff"
            if staff
            else "Add Staff"
        )

        self.setMinimumWidth(500)

        layout = QFormLayout(self)

        #
        # First Name
        #

        self.first_name_edit = QLineEdit()

        layout.addRow(
            "First Name",
            self.first_name_edit,
        )

        #
        # Last Name
        #

        self.last_name_edit = QLineEdit()

        layout.addRow(
            "Last Name",
            self.last_name_edit,
        )

        #
        # Email
        #

        self.email_edit = QLineEdit()

        layout.addRow(
            "Email",
            self.email_edit,
        )

        #
        # Phone
        #

        self.phone_edit = QLineEdit()

        layout.addRow(
            "Phone",
            self.phone_edit,
        )

        #
        # Job Title
        #

        self.job_title_edit = QLineEdit()

        layout.addRow(
            "Job Title",
            self.job_title_edit,
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
        # Employment Type
        #

        self.employment_type_combo = QComboBox()

        self.employment_type_combo.addItems(
            [
                "Full-Time",
                "Part-Time",
                "Contract",
                "Temporary",
            ]
        )

        layout.addRow(
            "Employment Type",
            self.employment_type_combo,
        )

        #
        # Contract Details
        #

        self.contract_details_edit = QPlainTextEdit()

        self.contract_details_edit.setFixedHeight(
            80,
        )

        layout.addRow(
            "Contract Details",
            self.contract_details_edit,
        )

        #
        # Salary
        #

        self.salary_spin = QDoubleSpinBox()

        self.salary_spin.setDecimals(2)

        self.salary_spin.setMaximum(
            1_000_000.00,
        )

        layout.addRow(
            "Salary",
            self.salary_spin,
        )

        #
        # Emergency Contact Name
        #

        self.emergency_contact_name_edit = QLineEdit()

        layout.addRow(
            "Emergency Contact Name",
            self.emergency_contact_name_edit,
        )

        #
        # Emergency Contact Phone
        #

        self.emergency_contact_phone_edit = QLineEdit()

        layout.addRow(
            "Emergency Contact Phone",
            self.emergency_contact_phone_edit,
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

        layout.addRow(
            buttons,
        )

        if staff:

            self._load_staff()

    def _load_staff(self) -> None:
        """
        Populate dialog with existing staff.
        """

        staff = self._staff

        if staff is None:
            return

        self.first_name_edit.setText(
            staff.first_name,
        )

        self.last_name_edit.setText(
            staff.last_name,
        )

        self.email_edit.setText(
            staff.email,
        )

        self.phone_edit.setText(
            staff.phone or "",
        )

        self.job_title_edit.setText(
            staff.job_title,
        )

        self.contract_details_edit.setPlainText(
            staff.contract_details or "",
        )

        self.salary_spin.setValue(
            float(staff.salary or 0),
        )

        self.emergency_contact_name_edit.setText(
            staff.emergency_contact_name or "",
        )

        self.emergency_contact_phone_edit.setText(
            staff.emergency_contact_phone or "",
        )

        self._select_combo_data(
            self.department_combo,
            staff.department_id,
        )

        if staff.employment_type:

            index = (
                self.employment_type_combo.findText(
                    staff.employment_type,
                )
            )

            if index >= 0:

                self.employment_type_combo.setCurrentIndex(
                    index,
                )

    @staticmethod
    def _select_combo_data(
        combo: QComboBox,
        value,
    ) -> None:
        """
        Select a combo item by its userData.
        """

        for i in range(combo.count()):

            if combo.itemData(i) == value:

                combo.setCurrentIndex(i)

                return

    def _validate(self) -> None:
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

        if not self.job_title_edit.text().strip():

            QMessageBox.warning(
                self,
                "Validation Error",
                "Job title is required.",
            )

            return

        self.accept()

    def get_staff_data(self) -> dict:
        """
        Return the entered staff data.
        """

        return {
            "first_name": (
                self.first_name_edit.text().strip()
            ),
            "last_name": (
                self.last_name_edit.text().strip()
            ),
            "email": (
                self.email_edit.text().strip()
            ),
            "phone": (
                self.phone_edit.text().strip()
                or None
            ),
            "job_title": (
                self.job_title_edit.text().strip()
            ),
            "department_id": (
                self.department_combo.currentData()
            ),
            "employment_type": (
                self.employment_type_combo.currentText()
            ),
            "contract_details": (
                self.contract_details_edit
                .toPlainText()
                .strip()
                or None
            ),
            "salary": (
                Decimal(
                    str(
                        self.salary_spin.value()
                    )
                )
            ),
            "emergency_contact_name": (
                self.emergency_contact_name_edit
                .text()
                .strip()
                or None
            ),
            "emergency_contact_phone": (
                self.emergency_contact_phone_edit
                .text()
                .strip()
                or None
            ),
        }