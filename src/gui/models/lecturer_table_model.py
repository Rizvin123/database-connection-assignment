"""
Table model for displaying lecturers.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt

from src.models.lecturer import Lecturer


class LecturerTableModel(QAbstractTableModel):
    """
    Table model for Lecturer objects.
    """

    HEADERS = [
        "ID",
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Department",
        "Course Load",
        "Research Group",
        "Office",
    ]

    def __init__(
        self,
        lecturers: list[Lecturer] | None = None,
    ) -> None:
        """
        Initialise the model.
        """

        super().__init__()

        self._lecturers = lecturers or []

    def rowCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:
        """
        Return the number of rows.
        """

        return len(self._lecturers)

    def columnCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:
        """
        Return the number of columns.
        """

        return len(self.HEADERS)

    def data(
        self,
        index: QModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        """
        Return the data for a table cell.
        """

        if (
            not index.isValid()
            or role != Qt.ItemDataRole.DisplayRole
        ):
            return None

        lecturer = self._lecturers[index.row()]

        column = index.column()

        if column == 0:
            return lecturer.lecturer_id

        if column == 1:
            return lecturer.first_name

        if column == 2:
            return lecturer.last_name

        if column == 3:
            return lecturer.email

        if column == 4:
            return lecturer.phone

        if column == 5:
            return (
                lecturer.department.department_name
                if lecturer.department
                else ""
            )

        if column == 6:
            return lecturer.course_load

        if column == 7:
            return (
                lecturer.research_group.group_name
                if lecturer.research_group
                else ""
            )

        if column == 8:
            return lecturer.office_room

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        """
        Return header labels.
        """

        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return self.HEADERS[section]

        return super().headerData(
            section,
            orientation,
            role,
        )

    def lecturer_at(
        self,
        row: int,
    ) -> Lecturer:
        """
        Return the lecturer at the specified row.
        """

        return self._lecturers[row]

    def set_lecturers(
        self,
        lecturers: list[Lecturer],
    ) -> None:
        """
        Replace the lecturers displayed by the model.
        """

        self.beginResetModel()

        self._lecturers = lecturers

        self.endResetModel()

    def refresh(
        self,
    ) -> None:
        """
        Notify views that the model data has changed.
        """

        self.beginResetModel()

        self.endResetModel()