"""
Lecturer management widget.
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

from src.gui.dialogs.lecturer_dialog import LecturerDialog
from src.models.lecturer import Lecturer


from src.database.session import SessionLocal
from src.gui.models.lecturer_table_model import LecturerTableModel
from src.repositories.department_repository import DepartmentRepository
from src.repositories.lecturer_repository import LecturerRepository
from src.repositories.research_group_repository import (
    ResearchGroupRepository,
)
from src.services.lecturer_service import LecturerService


class LecturerWidget(QWidget):
    """
    Widget for displaying and managing lecturers.
    """

    def __init__(self) -> None:
        super().__init__()

        #
        # Database layer
        #

        self._session = SessionLocal()

        self._lecturer_repository = LecturerRepository(
            self._session,
        )

        self._service = LecturerService(
            self._session,
        )

        self._department_repository = DepartmentRepository(
            self._session,
        )

        self._research_group_repository = (
            ResearchGroupRepository(
                self._session,
            )
        )

        #
        # UI
        #

        self._build_ui()

        self.load_lecturers()

        self.load_filters()

    def _build_ui(
        self,
    ) -> None:
        """
        Create the user interface.
        """

        main_layout = QVBoxLayout(self)

        #
        # Title
        #

        title = QLabel("Lecturers")

        title.setStyleSheet(
            """
            font-size:22px;
            font-weight:bold;
            """
        )

        main_layout.addWidget(title)

        #
        # Search & Filters
        #

        search_group = QGroupBox(
            "Search & Filters"
        )

        search_layout = QFormLayout(
            search_group,
        )

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

        self.department_filter = QComboBox()

        self.research_group_filter = QComboBox()

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
            "Research Group",
            self.research_group_filter,
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

        self.model = LecturerTableModel()

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

        self.add_button = QPushButton(
            "Add"
        )

        self.edit_button = QPushButton(
            "Edit"
        )

        self.delete_button = QPushButton(
            "Delete"
        )

        self.refresh_button = QPushButton(
            "Refresh"
        )

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
            self.load_lecturers,
        )

        self.clear_button.clicked.connect(
            self.clear_filters,
        )

        self.search_edit.returnPressed.connect(
            self.search_lecturers,
        )

        self.search_field_combo.currentIndexChanged.connect(
            self.search_lecturers,
        )

        self.department_filter.currentIndexChanged.connect(
            self.search_lecturers,
        )

        self.research_group_filter.currentIndexChanged.connect(
            self.search_lecturers,
        )

        self.add_button.clicked.connect(
            self.add_lecturer,
        )

        self.edit_button.clicked.connect(
            self.edit_lecturer,
        )

        self.delete_button.clicked.connect(
            self.delete_lecturer,
        )

    def load_lecturers(
        self,
    ) -> None:
        """
        Load lecturers from the database.
        """

        lecturers = self._service.get_all_lecturers()

        self.model.set_lecturers(
            lecturers,
        )

        self.status_label.setText(
            f"{len(lecturers)} lecturer(s)"
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

    def load_filters(self) -> None:
        """
        Populate filter combo boxes.
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

        self.research_group_filter.clear()

        self.research_group_filter.addItem(
            "All Research Groups",
            None,
        )

        for group in (
            self._research_group_repository.get_research_groups()
        ):

            self.research_group_filter.addItem(
                group.group_name,
                group.research_group_id,
            )

    def add_lecturer(self) -> None:
        """
        Open the Add Lecturer dialog.
        """

        departments = (
            self._department_repository.get_department_names()
        )

        research_groups = (
            self._research_group_repository.get_research_groups()
        )

        dialog = LecturerDialog(
            departments=departments,
            research_groups=research_groups,
        )

        if not dialog.exec():
            return

        data = dialog.get_lecturer_data()

        lecturer = Lecturer(**data)

        try:

            self._service.create_lecturer(
                lecturer,
            )

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Unable to Create Lecturer",
                str(exc),
            )

            return

        self.load_lecturers()

        QMessageBox.information(
            self,
            "Success",
            "Lecturer added successfully.",
        )

    def selected_lecturer(self) -> Lecturer | None:
        """
        Return the currently selected lecturer.
        """

        selection = (
            self.table.selectionModel()
            .selectedRows()
        )

        if not selection:
            return None

        row = selection[0].row()

        return self.model.lecturer_at(row)
    
    def edit_lecturer(self) -> None:
        """
        Edit the selected lecturer.
        """

        lecturer = self.selected_lecturer()

        if lecturer is None:

            QMessageBox.information(
                self,
                "Edit Lecturer",
                "Please select a lecturer.",
            )

            return

        departments = (
            self._department_repository.get_department_names()
        )

        research_groups = (
            self._research_group_repository.get_research_groups()
        )

        dialog = LecturerDialog(
            departments=departments,
            research_groups=research_groups,
            lecturer=lecturer,
        )

        if not dialog.exec():
            return

        data = dialog.get_lecturer_data()

        lecturer.first_name = data["first_name"]
        lecturer.last_name = data["last_name"]
        lecturer.email = data["email"]
        lecturer.phone = data["phone"]
        lecturer.department_id = data["department_id"]
        lecturer.course_load = data["course_load"]
        lecturer.research_group_id = data["research_group_id"]
        lecturer.office_room = data["office_room"]

        try:

            self._service.update_lecturer()

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Update Failed",
                str(exc),
            )

            return

        self.load_lecturers()

        QMessageBox.information(
            self,
            "Success",
            "Lecturer updated successfully.",
        )

    def delete_lecturer(self) -> None:
        """
        Delete the selected lecturer.
        """

        lecturer = self.selected_lecturer()

        if lecturer is None:

            QMessageBox.information(
                self,
                "Delete Lecturer",
                "Please select a lecturer.",
            )

            return

        answer = QMessageBox.question(
            self,
            "Delete Lecturer",
            (
                f"Delete "
                f"{lecturer.first_name} "
                f"{lecturer.last_name}?"
            ),
            QMessageBox.StandardButton.Yes
            |
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:

            self._service.delete_lecturer(
                lecturer.lecturer_id,
            )

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Delete Failed",
                str(exc),
            )

            return

        self.load_lecturers()

        QMessageBox.information(
            self,
            "Success",
            "Lecturer deleted successfully.",
        )

    def search_lecturers(self, *args) -> None:
        """
        Search lecturers.
        """

        lecturers = self._service.search_lecturers(
            search_field=self.search_field_combo.currentData(),
            search_text=self.search_edit.text(),
            department_id=self.department_filter.currentData(),
            research_group_id=self.research_group_filter.currentData(),
        )

        self.model.set_lecturers(
            lecturers,
        )

        self.status_label.setText(
            f"{len(lecturers)} lecturer(s)"
        )

    def clear_filters(self) -> None:
        """
        Reset every search control.
        """

        self.search_field_combo.blockSignals(True)
        self.department_filter.blockSignals(True)
        self.research_group_filter.blockSignals(True)

        self.search_field_combo.setCurrentIndex(0)
        self.search_edit.clear()
        self.department_filter.setCurrentIndex(0)
        self.research_group_filter.setCurrentIndex(0)

        self.search_field_combo.blockSignals(False)
        self.department_filter.blockSignals(False)
        self.research_group_filter.blockSignals(False)

        self.load_lecturers()