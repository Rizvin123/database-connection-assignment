"""
Research Group management widget.
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

from src.gui.dialogs.research_group_dialog import (
    ResearchGroupDialog,
)
from src.models.research_group import ResearchGroup

from src.database.session import SessionLocal
from src.gui.models.research_group_table_model import (
    ResearchGroupTableModel,
)
from src.repositories.department_repository import (
    DepartmentRepository,
)
from src.repositories.lecturer_repository import (
    LecturerRepository,
)
from src.services.research_group_service import (
    ResearchGroupService,
)


class ResearchGroupWidget(QWidget):
    """
    Widget for displaying and managing research groups.
    """

    def __init__(self) -> None:
        super().__init__()

        #
        # Database layer
        #

        self._session = SessionLocal()

        self._service = ResearchGroupService(
            self._session,
        )

        self._department_repository = (
            DepartmentRepository(
                self._session,
            )
        )

        self._lecturer_repository = (
            LecturerRepository(
                self._session,
            )
        )

        #
        # UI
        #

        self._build_ui()

        self.load_research_groups()

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

        title = QLabel(
            "Research Groups",
        )

        title.setStyleSheet(
            """
            font-size:22px;
            font-weight:bold;
            """
        )

        main_layout.addWidget(
            title,
        )

        #
        # Search & Filters
        #

        search_group = QGroupBox(
            "Search & Filters",
        )

        search_layout = QFormLayout(
            search_group,
        )

        self.search_edit = QLineEdit()

        self.department_filter = (
            QComboBox()
        )

        self.head_lecturer_filter = (
            QComboBox()
        )

        self.clear_button = QPushButton(
            "Clear",
        )

        search_layout.addRow(
            "Group Name",
            self.search_edit,
        )

        search_layout.addRow(
            "Department",
            self.department_filter,
        )

        search_layout.addRow(
            "Head Lecturer",
            self.head_lecturer_filter,
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

        self.model = (
            ResearchGroupTableModel()
        )

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
            "Add",
        )

        self.edit_button = QPushButton(
            "Edit",
        )

        self.delete_button = QPushButton(
            "Delete",
        )

        self.refresh_button = QPushButton(
            "Refresh",
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
            self.load_research_groups,
        )

        self.add_button.clicked.connect(
            self.add_research_group,
        )

        self.edit_button.clicked.connect(
            self.edit_research_group,
        )

        self.delete_button.clicked.connect(
            self.delete_research_group,
        )

        self.clear_button.clicked.connect(
            self.clear_filters,
        )

        self.search_edit.returnPressed.connect(
            self.search_research_groups,
        )

        self.department_filter.currentIndexChanged.connect(
            self.search_research_groups,
        )

        self.head_lecturer_filter.currentIndexChanged.connect(
            self.search_research_groups,
        )

    def load_research_groups(
        self,
    ) -> None:
        """
        Load research groups.
        """

        self._session.expire_all()

        groups = (
            self._service.get_all_research_groups()
        )

        self.model.set_research_groups(
            groups,
        )

        self.status_label.setText(
            f"{len(groups)} research group(s)"
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
            self._department_repository
            .get_department_names()
        ):

            self.department_filter.addItem(
                department.department_name,
                department.department_id,
            )

        #
        # Head Lecturers
        #

        self.head_lecturer_filter.clear()

        self.head_lecturer_filter.addItem(
            "All Head Lecturers",
            None,
        )

        lecturers = (
            self._lecturer_repository
            .get_all()
        )

        lecturers.sort(
            key=lambda lecturer: (
                lecturer.last_name,
                lecturer.first_name,
            )
        )

        for lecturer in lecturers:

            self.head_lecturer_filter.addItem(
                f"{lecturer.first_name} "
                f"{lecturer.last_name}",
                lecturer.lecturer_id,
            )

    def closeEvent(
        self,
        event,
    ) -> None:
        """
        Close the database session.
        """

        self._session.close()

        super().closeEvent(
            event,
        )

    def selected_research_group(
    self,
    ) -> ResearchGroup | None:
        """
        Return the selected research group.
        """

        selection = (
            self.table.selectionModel()
            .selectedRows()
        )

        if not selection:

            return None

        return self.model.research_group_at(
            selection[0].row(),
        )
    
    def add_research_group(
    self,
) -> None:
        """
        Add a research group.
        """

        departments = (
            self._department_repository.get_department_names()
        )

        lecturers = (
            self._lecturer_repository.get_all()
        )

        dialog = ResearchGroupDialog(
            departments=departments,
            lecturers=lecturers,
        )

        if not dialog.exec():

            return

        data = dialog.get_research_group_data()

        group = ResearchGroup(
            **data,
        )

        try:

            self._service.create_research_group(
                group,
            )

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Unable to Create Research Group",
                str(exc),
            )

            return

        self.load_research_groups()

        self.load_filters()

        QMessageBox.information(
            self,
            "Success",
            "Research group added successfully.",
        )

    def edit_research_group(
    self,
    ) -> None:
        """
        Edit the selected research group.
        """

        group = self.selected_research_group()

        if group is None:

            QMessageBox.information(
                self,
                "Edit Research Group",
                "Please select a research group.",
            )

            return

        departments = (
            self._department_repository.get_department_names()
        )

        lecturers = (
            self._lecturer_repository.get_all()
        )

        dialog = ResearchGroupDialog(
            departments=departments,
            lecturers=lecturers,
            research_group=group,
        )

        if not dialog.exec():

            return

        data = dialog.get_research_group_data()

        group.group_name = data["group_name"]

        group.department_id = data["department_id"]

        group.head_lecturer_id = (
            data["head_lecturer_id"]
        )

        try:

            self._service.update_research_group()

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Update Failed",
                str(exc),
            )

            return

        self.load_research_groups()

        self.load_filters()

        QMessageBox.information(
            self,
            "Success",
            "Research group updated successfully.",
        )

    def delete_research_group(
        self,
    ) -> None:
        """
        Delete the selected research group.
        """

        group = self.selected_research_group()

        if group is None:

            QMessageBox.information(
                self,
                "Delete Research Group",
                "Please select a research group.",
            )

            return

        answer = QMessageBox.question(
            self,
            "Delete Research Group",
            (
                f"Delete "
                f"{group.group_name}?"
            ),
            QMessageBox.StandardButton.Yes
            |
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:

            return

        try:

            self._service.delete_research_group(
                group.research_group_id,
            )

        except ValueError as exc:

            QMessageBox.warning(
                self,
                "Delete Failed",
                str(exc),
            )

            return

        self.load_research_groups()

        self.load_filters()

        QMessageBox.information(
            self,
            "Success",
            "Research group deleted successfully.",
        )

    def search_research_groups(
        self,
        *args,
    ) -> None:
        """
        Search research groups.
        """

        self._session.expire_all()

        groups = self._service.search_research_groups(
            search_text=self.search_edit.text().strip(),
            department_id=self.department_filter.currentData(),
            head_lecturer_id=self.head_lecturer_filter.currentData(),
        )

        self.model.set_research_groups(
            groups,
        )

        self.status_label.setText(
            f"{len(groups)} research group(s)"
        )

    def clear_filters(
        self,
    ) -> None:
        """
        Reset all search controls.
        """

        self.department_filter.blockSignals(True)

        self.head_lecturer_filter.blockSignals(True)

        self.search_edit.clear()

        self.department_filter.setCurrentIndex(0)

        self.head_lecturer_filter.setCurrentIndex(0)

        self.department_filter.blockSignals(False)

        self.head_lecturer_filter.blockSignals(False)

        self.load_research_groups()