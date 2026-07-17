"""
Dialog for adding and editing lecturers.
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QSpinBox,
)

from src.models.department import Department
from src.models.lecturer import Lecturer
from src.models.research_group import ResearchGroup


class LecturerDialog(QDialog):
    """
    Dialog used to create or edit a lecturer.
    """

    def __init__(
        self,
        departments: list[Department],
        research_groups: list[ResearchGroup],
        lecturer: Lecturer | None = None,
    ) -> None:
        super().__init__()

        self._lecturer = lecturer

        self.setWindowTitle(
            "Edit Lecturer"
            if lecturer
            else "Add Lecturer"
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
        # Course Load
        #

        self.course_load_spin = QSpinBox()

        self.course_load_spin.setMinimum(0)

        self.course_load_spin.setMaximum(50)

        layout.addRow(
            "Course Load",
            self.course_load_spin,
        )

        #
        # Research Group
        #

        self.research_group_combo = QComboBox()

        self.research_group_combo.addItem(
            "None",
            None,
        )

        for group in research_groups:

            self.research_group_combo.addItem(
                group.group_name,
                group.research_group_id,
            )

        layout.addRow(
            "Research Group",
            self.research_group_combo,
        )

        #
        # Office Room
        #

        self.office_room_edit = QLineEdit()

        layout.addRow(
            "Office Room",
            self.office_room_edit,
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

        if lecturer:

            self._load_lecturer()

    def _load_lecturer(
        self,
    ) -> None:
        """
        Populate the dialog with an existing lecturer's data.
        """

        lecturer = self._lecturer

        if lecturer is None:
            return

        self.first_name_edit.setText(
            lecturer.first_name,
        )

        self.last_name_edit.setText(
            lecturer.last_name,
        )

        self.email_edit.setText(
            lecturer.email,
        )

        self.phone_edit.setText(
            lecturer.phone or "",
        )

        self.course_load_spin.setValue(
            lecturer.course_load,
        )

        self.office_room_edit.setText(
            lecturer.office_room or "",
        )

        self._select_combo_data(
            self.department_combo,
            lecturer.department_id,
        )

        self._select_combo_data(
            self.research_group_combo,
            lecturer.research_group_id,
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

    def get_lecturer_data(
        self,
    ) -> dict:
        """
        Return the entered lecturer data.
        """

        return {
            "first_name": self.first_name_edit.text().strip(),
            "last_name": self.last_name_edit.text().strip(),
            "email": self.email_edit.text().strip(),
            "phone": self.phone_edit.text().strip() or None,
            "department_id": self.department_combo.currentData(),
            "course_load": self.course_load_spin.value(),
            "research_group_id": self.research_group_combo.currentData(),
            "office_room": self.office_room_edit.text().strip() or None,
        }