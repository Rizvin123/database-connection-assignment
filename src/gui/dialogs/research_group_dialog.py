"""
Dialog for adding and editing research groups.
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
)

from src.models.department import Department
from src.models.lecturer import Lecturer
from src.models.research_group import ResearchGroup


class ResearchGroupDialog(QDialog):
    """
    Dialog used to create or edit a research group.
    """

    def __init__(
        self,
        departments: list[Department],
        lecturers: list[Lecturer],
        research_group: ResearchGroup | None = None,
    ) -> None:
        super().__init__()

        self._research_group = research_group

        self.setWindowTitle(
            "Edit Research Group"
            if research_group
            else "Add Research Group"
        )

        self.setMinimumWidth(450)

        layout = QFormLayout(self)

        #
        # Group Name
        #

        self.group_name_edit = QLineEdit()

        layout.addRow(
            "Group Name",
            self.group_name_edit,
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
        # Head Lecturer
        #

        self.head_lecturer_combo = QComboBox()

        self.head_lecturer_combo.addItem(
            "No Head Lecturer",
            None,
        )

        for lecturer in lecturers:

            self.head_lecturer_combo.addItem(
                f"{lecturer.first_name} "
                f"{lecturer.last_name}",
                lecturer.lecturer_id,
            )

        layout.addRow(
            "Head Lecturer",
            self.head_lecturer_combo,
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

        if research_group:

            self._load_research_group()

    def _load_research_group(
        self,
    ) -> None:
        """
        Populate the dialog from an existing research group.
        """

        group = self._research_group

        if group is None:

            return

        self.group_name_edit.setText(
            group.group_name,
        )

        self._select_combo_data(
            self.department_combo,
            group.department_id,
        )

        self._select_combo_data(
            self.head_lecturer_combo,
            group.head_lecturer_id,
        )

    @staticmethod
    def _select_combo_data(
        combo: QComboBox,
        value,
    ) -> None:
        """
        Select a combo item by its user data.
        """

        for index in range(
            combo.count()
        ):

            if combo.itemData(index) == value:

                combo.setCurrentIndex(
                    index,
                )

                return

    def _validate(
        self,
    ) -> None:
        """
        Validate required fields.
        """

        if not self.group_name_edit.text().strip():

            QMessageBox.warning(
                self,
                "Validation Error",
                "Group name is required.",
            )

            return

        self.accept()

    def get_research_group_data(
        self,
    ) -> dict:
        """
        Return the entered research group data.
        """

        return {
            "group_name":
                self.group_name_edit
                .text()
                .strip(),

            "department_id":
                self.department_combo
                .currentData(),

            "head_lecturer_id":
                self.head_lecturer_combo
                .currentData(),
        }