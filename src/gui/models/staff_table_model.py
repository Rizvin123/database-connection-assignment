"""
Table model for displaying staff members.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)

from src.models.staff import Staff


class StaffTableModel(QAbstractTableModel):
    """
    Table model for Staff objects.
    """

    HEADERS = [
        "ID",
        "First Name",
        "Last Name",
        "Email",
        "Job Title",
        "Department",
        "Employment Type",
    ]

    def __init__(
        self,
        staff: list[Staff] | None = None,
    ) -> None:
        """
        Initialise the model.
        """

        super().__init__()

        self._staff = staff or []

    def rowCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:
        """
        Return the number of rows.
        """

        return len(
            self._staff,
        )

    def columnCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:
        """
        Return the number of columns.
        """

        return len(
            self.HEADERS,
        )

    def data(
        self,
        index: QModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        """
        Return data for the table.
        """

        if (
            not index.isValid()
            or role != Qt.ItemDataRole.DisplayRole
        ):
            return None

        staff = self._staff[
            index.row()
        ]

        column = index.column()

        if column == 0:
            return staff.staff_id

        if column == 1:
            return staff.first_name

        if column == 2:
            return staff.last_name

        if column == 3:
            return staff.email

        if column == 4:
            return staff.job_title

        if column == 5:
            return (
                staff.department.department_name
                if staff.department
                else ""
            )

        if column == 6:
            return (
                staff.employment_type
                or ""
            )

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        """
        Return column headers.
        """

        if (
            orientation
            == Qt.Orientation.Horizontal
            and role
            == Qt.ItemDataRole.DisplayRole
        ):
            return self.HEADERS[
                section
            ]

        return super().headerData(
            section,
            orientation,
            role,
        )

    def staff_at(
        self,
        row: int,
    ) -> Staff:
        """
        Return the staff member at a row.
        """

        return self._staff[
            row
        ]

    def set_staff(
        self,
        staff: list[Staff],
    ) -> None:
        """
        Replace the displayed staff.
        """

        self.beginResetModel()

        self._staff = staff

        self.endResetModel()

    def refresh(
        self,
    ) -> None:
        """
        Refresh the model.
        """

        self.beginResetModel()

        self.endResetModel()