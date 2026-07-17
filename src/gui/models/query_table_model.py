"""
Generic table model for displaying query results.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)


class QueryTableModel(
    QAbstractTableModel,
):
    """
    Generic table model used by the Queries page.
    """

    def __init__(
        self,
    ) -> None:
        super().__init__()

        self._headers: list[str] = []

        self._rows: list[list[Any]] = []

    def rowCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:

        return len(
            self._rows,
        )

    def columnCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:

        return len(
            self._headers,
        )

    def data(
        self,
        index: QModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:

        if (
            not index.isValid()
            or role != Qt.ItemDataRole.DisplayRole
        ):

            return None

        return self._rows[
            index.row()
        ][
            index.column()
        ]

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:

        if (
            orientation
            == Qt.Orientation.Horizontal
            and role
            == Qt.ItemDataRole.DisplayRole
        ):

            return self._headers[
                section
            ]

        return super().headerData(
            section,
            orientation,
            role,
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all data.
        """

        self.beginResetModel()

        self._headers.clear()

        self._rows.clear()

        self.endResetModel()

    def set_results(
        self,
        headers: list[str],
        rows: list[list[Any]],
    ) -> None:
        """
        Replace displayed query results.
        """

        self.beginResetModel()

        self._headers = headers

        self._rows = rows

        self.endResetModel()

    def row(
        self,
        index: int,
    ) -> list[Any]:
        """
        Return one row.
        """

        return self._rows[
            index
        ]