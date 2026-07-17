"""
Table model for displaying research groups.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)

from src.models.research_group import ResearchGroup


class ResearchGroupTableModel(
    QAbstractTableModel,
):
    """
    Table model for ResearchGroup objects.
    """

    HEADERS = [
        "ID",
        "Group Name",
        "Department",
        "Head Lecturer",
    ]

    def __init__(
        self,
        research_groups: list[ResearchGroup] | None = None,
    ) -> None:
        """
        Initialise the model.
        """

        super().__init__()

        self._research_groups = (
            research_groups or []
        )

    def rowCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:
        """
        Return the number of rows.
        """

        return len(
            self._research_groups,
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

        group = self._research_groups[
            index.row()
        ]

        column = index.column()

        if column == 0:
            return group.research_group_id

        if column == 1:
            return group.group_name

        if column == 2:

            return (
                group.department.department_name
                if group.department
                else ""
            )

        if column == 3:

            if group.head_lecturer:

                return (
                    f"{group.head_lecturer.first_name} "
                    f"{group.head_lecturer.last_name}"
                )

            return ""

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        """
        Return table headers.
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

    def research_group_at(
        self,
        row: int,
    ) -> ResearchGroup:
        """
        Return the research group at a row.
        """

        return self._research_groups[
            row
        ]

    def set_research_groups(
        self,
        research_groups: list[ResearchGroup],
    ) -> None:
        """
        Replace displayed research groups.
        """

        self.beginResetModel()

        self._research_groups = (
            research_groups
        )

        self.endResetModel()

    def refresh(
        self,
    ) -> None:
        """
        Refresh the model.
        """

        self.beginResetModel()

        self.endResetModel()