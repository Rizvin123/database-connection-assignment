"""
Staff management widget.
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

from src.gui.dialogs.staff_dialog import StaffDialog
from src.models.staff import Staff

from src.database.session import SessionLocal
from src.gui.models.staff_table_model import StaffTableModel
from src.repositories.department_repository import DepartmentRepository
from src.repositories.staff_repository import StaffRepository
from src.services.staff_service import StaffService


class StaffWidget(QWidget):
    """
    Widget for displaying and managing staff.
    """

    def __init__(self) -> None:
        super().__init__()

        #
        # Database layer
        #

        self._session = SessionLocal()

        self._staff_repository = StaffRepository(
            self._session,
        )

        self._department_repository = DepartmentRepository(
            self._session,
        )

        self._service = StaffService(
            self._session,
        )

        #
        # UI
        #

        self._build_ui()

        self.load_staff()

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

        title = QLabel("Staff")

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

        self.job_title_filter = QComboBox()

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
            "Job Title",
            self.job_title_filter,
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

        self.model = StaffTableModel()

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
            self.load_staff,
        )

        self.add_button.clicked.connect(
            self.add_staff,
        )

        self.edit_button.clicked.connect(
            self.edit_staff,
        )

        self.delete_button.clicked.connect(
            self.delete_staff,
        )

        self.clear_button.clicked.connect(
            self.clear_filters,
        )

        self.search_edit.returnPressed.connect(
            self.search_staff,
        )

        self.search_field_combo.currentIndexChanged.connect(
            self.search_staff,
        )

        self.department_filter.currentIndexChanged.connect(
            self.search_staff,
        )

        self.job_title_filter.currentIndexChanged.connect(
            self.search_staff,
        )

    def load_staff(
        self,
    ) -> None:
        """
        Load staff from the database.
        """

        staff = self._service.get_all_staff()

        self.model.set_staff(
            staff,
        )

        self.status_label.setText(
            f"{len(staff)} staff member(s)"
        )

    def load_filters(
        self,
    ) -> None:
        """
        Populate filter controls.
        """

        #
        # Departments
        #

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

        #
        # Job Titles
        #

        self.job_title_filter.clear()

        self.job_title_filter.addItem(
            "All Job Titles",
            None,
        )

        job_titles = sorted(
            {
                staff.job_title
                for staff in self._service.get_all_staff()
                if staff.job_title
            }
        )

        for title in job_titles:

            self.job_title_filter.addItem(
                title,
                title,
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

    def selected_staff(
        self,
    ) -> Staff | None:
        """
        Return the selected staff member.
        """

        selection = (
            self.table.selectionModel()
            .selectedRows()
        )

        if not selection:
            return None

        return self.model.staff_at(
            selection[0].row(),
        )
    

    def add_staff(
    self,
) -> None:
        """
        Add a new staff member.
        """

        departments = (
            self._department_repository.get_department_names()
        )

        dialog = StaffDialog(
            departments=departments,
        )

        if not dialog.exec():
            return

        data = dialog.get_staff_data()

        staff = Staff(**data)

        try:

            self._service.create_staff(
                staff,
            )

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Unable to Create Staff",
                str(exc),
            )

            return

        self.load_staff()
        self.load_filters()

        QMessageBox.information(
            self,
            "Success",
            "Staff member added successfully.",
        )

    def edit_staff(
    self,
) -> None:
        """
        Edit the selected staff member.
        """

        staff = self.selected_staff()

        if staff is None:

            QMessageBox.information(
                self,
                "Edit Staff",
                "Please select a staff member.",
            )

            return

        departments = (
            self._department_repository.get_department_names()
        )

        dialog = StaffDialog(
            departments=departments,
            staff=staff,
        )

        if not dialog.exec():
            return

        data = dialog.get_staff_data()

        staff.first_name = data["first_name"]
        staff.last_name = data["last_name"]
        staff.email = data["email"]
        staff.phone = data["phone"]
        staff.job_title = data["job_title"]
        staff.department_id = data["department_id"]
        staff.employment_type = data["employment_type"]
        staff.contract_details = data["contract_details"]
        staff.salary = data["salary"]
        staff.emergency_contact_name = (
            data["emergency_contact_name"]
        )
        staff.emergency_contact_phone = (
            data["emergency_contact_phone"]
        )

        try:

            self._service.update_staff()

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Update Failed",
                str(exc),
            )

            return

        self.load_staff()
        self.load_filters()

        QMessageBox.information(
            self,
            "Success",
            "Staff member updated successfully.",
        )

    def delete_staff(
    self,
) -> None:
        """
        Delete the selected staff member.
        """

        staff = self.selected_staff()

        if staff is None:

            QMessageBox.information(
                self,
                "Delete Staff",
                "Please select a staff member.",
            )

            return

        answer = QMessageBox.question(
            self,
            "Delete Staff",
            (
                f"Delete "
                f"{staff.first_name} "
                f"{staff.last_name}?"
            ),
            QMessageBox.StandardButton.Yes
            |
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:

            self._service.delete_staff(
                staff.staff_id,
            )

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Delete Failed",
                str(exc),
            )

            return

        self.load_staff()
        self.load_filters()

        QMessageBox.information(
            self,
            "Success",
            "Staff member deleted successfully.",
        )

    def search_staff(
    self,
    *args,
) -> None:
        """
        Search staff.
        """

        staff = self._service.search_staff(
            search_field=self.search_field_combo.currentData(),
            search_text=self.search_edit.text().strip(),
            department_id=self.department_filter.currentData(),
            job_title=self.job_title_filter.currentData(),
        )

        self.model.set_staff(
            staff,
        )

        self.status_label.setText(
            f"{len(staff)} staff member(s)"
        )

    def clear_filters(
    self,
) -> None:
        """
        Reset all search controls.
        """

        self.search_field_combo.blockSignals(True)

        self.department_filter.blockSignals(True)

        self.job_title_filter.blockSignals(True)

        self.search_field_combo.setCurrentIndex(0)

        self.search_edit.clear()

        self.department_filter.setCurrentIndex(0)

        self.job_title_filter.setCurrentIndex(0)

        self.search_field_combo.blockSignals(False)

        self.department_filter.blockSignals(False)

        self.job_title_filter.blockSignals(False)

        self.load_staff()