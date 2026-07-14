"""
Table model for displaying courses.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)

from src.models.course import Course


class CourseTableModel(QAbstractTableModel):
    """
    Table model for Course objects.
    """

    HEADERS = [
        "Course Code",
        "Course Name",
        "Department",
        "Level",
        "Credits",
        "Schedule",
    ]

    def __init__(
        self,
        courses: list[Course] | None = None,
    ) -> None:
        """
        Initialise the model.
        """

        super().__init__()

        self._courses = courses or []

    def rowCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:
        """
        Return the number of rows.
        """

        return len(self._courses)

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

        course = self._courses[index.row()]

        column = index.column()

        if column == 0:
            return course.course_code

        if column == 1:
            return course.course_name

        if column == 2:
            return (
                course.department.department_name
                if course.department
                else ""
            )

        if column == 3:
            return course.level

        if column == 4:
            return course.credits

        if column == 5:
            return course.schedule or ""

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

    def course_at(
        self,
        row: int,
    ) -> Course:
        """
        Return the course at the specified row.
        """

        return self._courses[row]

    def set_courses(
        self,
        courses: list[Course],
    ) -> None:
        """
        Replace the courses displayed by the model.
        """

        self.beginResetModel()

        self._courses = courses

        self.endResetModel()

    def refresh(
        self,
    ) -> None:
        """
        Notify views that the model data has changed.
        """

        self.beginResetModel()

        self.endResetModel()