"""
Qt table model for Student objects.
"""

from __future__ import annotations

from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt

from src.models.student import Student


class StudentTableModel(QAbstractTableModel):
    """
    Table model used to display Student records.
    """

    HEADERS = [
        "ID",
        "First Name",
        "Last Name",
        "Email",
        "Program",
        "Year",
        "Graduation Status",
    ]

    def __init__(
        self,
        students: list[Student] | None = None,
    ) -> None:
        super().__init__()

        self._students = students or []

    def rowCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:

        return len(self._students)

    def columnCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:

        return len(self.HEADERS)

    def data(
        self,
        index: QModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):

        if not index.isValid():
            return None

        if role != Qt.ItemDataRole.DisplayRole:
            return None

        student = self._students[index.row()]

        match index.column():

            case 0:
                return student.student_id

            case 1:
                return student.first_name

            case 2:
                return student.last_name

            case 3:
                return student.email

            case 4:
                if student.program:
                    return student.program.program_name

                return ""

            case 5:
                return student.year_of_study

            case 6:
                return student.graduation_status

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):

        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return self.HEADERS[section]

        return None

    def set_students(
        self,
        students: list[Student],
    ) -> None:
        """
        Replace the table contents.
        """

        self.beginResetModel()

        self._students = students

        self.endResetModel()

    def student_at(
        self,
        row: int,
    ) -> Student:
        """
        Return the Student at a given row.
        """

        return self._students[row]