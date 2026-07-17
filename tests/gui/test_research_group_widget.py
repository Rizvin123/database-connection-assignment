"""
GUI tests for ResearchGroupWidget.
"""

from __future__ import annotations

import uuid

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer

from PyQt6.QtWidgets import (
    QApplication,
    QDialogButtonBox,
    QMessageBox,
)
from src.models.research_group import ResearchGroup
from src.gui.dialogs.research_group_dialog import ResearchGroupDialog
from src.gui.widgets.research_group_widget import ResearchGroupWidget


def test_widget_loads(qtbot) -> None:
    """
    Verify the Research Group widget loads successfully.
    """

    widget = ResearchGroupWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.isVisible()


def test_table_populated(qtbot) -> None:
    """
    Verify the research group table is populated.
    """

    widget = ResearchGroupWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.model.rowCount() > 0


def test_status_label(qtbot) -> None:
    """
    Verify the status label displays the number of research groups.
    """

    widget = ResearchGroupWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert (
        "research group"
        in widget.status_label.text().lower()
    )

def test_add_research_group(qtbot) -> None:
    """
    Verify a research group can be added through the GUI.
    """

    widget = ResearchGroupWidget()

    qtbot.addWidget(widget)

    widget.show()

    initial_rows = widget.model.rowCount()

    group_name = f"GUI Research {uuid.uuid4()}"

    #
    # Fill dialog
    #

    def fill_dialog() -> None:

        dialog = None

        for window in QApplication.topLevelWidgets():

            if isinstance(
                window,
                ResearchGroupDialog,
            ):

                dialog = window

                break

        assert dialog is not None

        dialog.group_name_edit.setText(
            group_name,
        )

        #
        # Department
        #

        if dialog.department_combo.count() > 1:

            dialog.department_combo.setCurrentIndex(
                1,
            )

        #
        # Head Lecturer
        #

        if dialog.head_lecturer_combo.count() > 1:

            dialog.head_lecturer_combo.setCurrentIndex(
                1,
            )

        buttons = dialog.findChild(
            QDialogButtonBox,
        )

        save_button = buttons.button(
            QDialogButtonBox.StandardButton.Save,
        )

        qtbot.mouseClick(
            save_button,
            Qt.MouseButton.LeftButton,
        )

    #
    # Close success dialog
    #

    def close_message_box() -> None:

        for window in QApplication.topLevelWidgets():

            if isinstance(
                window,
                QMessageBox,
            ):

                ok_button = window.button(
                    QMessageBox.StandardButton.Ok,
                )

                if ok_button is not None:

                    qtbot.mouseClick(
                        ok_button,
                        Qt.MouseButton.LeftButton,
                    )

                    return

    #
    # Schedule helpers
    #

    QTimer.singleShot(
        0,
        fill_dialog,
    )

    QTimer.singleShot(
        500,
        close_message_box,
    )

    #
    # Click Add
    #

    widget.add_button.click()

    widget.load_research_groups()

    assert (
        widget.model.rowCount()
        == initial_rows + 1
    )

    group = widget._service.find_by_name(
        group_name,
    )

    assert group is not None

    assert (
        group.group_name
        == group_name
    )

    #
    # Cleanup
    #

    widget._service.delete_research_group(
        group.research_group_id,
    )

    widget.load_research_groups()

def test_edit_research_group(qtbot) -> None:
    """
   Verify a research group can be edited through the GUI.
    """

    widget = ResearchGroupWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.model.rowCount() > 0

    #
    # Select first row
    #

    widget.table.selectRow(0)

    qtbot.waitUntil(
        lambda: widget.selected_research_group() is not None,
        timeout=1000,
    )

    group = widget.selected_research_group()

    assert group is not None

    group_id = group.research_group_id

    original_name = group.group_name

    updated_name = "Edited GUI Research Group"

    #
    # Fill dialog
    #

    def fill_dialog() -> None:

        dialog = None

        for window in QApplication.topLevelWidgets():

            if isinstance(
                window,
                ResearchGroupDialog,
            ):

                dialog = window

                break

        assert dialog is not None

        dialog.group_name_edit.clear()

        dialog.group_name_edit.setText(
            updated_name,
        )

        buttons = dialog.findChild(
            QDialogButtonBox,
        )

        save_button = buttons.button(
            QDialogButtonBox.StandardButton.Save,
        )

        qtbot.mouseClick(
            save_button,
            Qt.MouseButton.LeftButton,
        )

    #
    # Close success dialog
    #

    def close_message_box() -> None:

        for window in QApplication.topLevelWidgets():

            if isinstance(
                window,
                QMessageBox,
            ):

                ok_button = window.button(
                    QMessageBox.StandardButton.Ok,
                )

                if ok_button is not None:

                    qtbot.mouseClick(
                        ok_button,
                        Qt.MouseButton.LeftButton,
                    )

                    return

    #
    # Schedule helpers
    #

    QTimer.singleShot(
        0,
        fill_dialog,
    )

    QTimer.singleShot(
        500,
        close_message_box,
    )

    #
    # Click Edit
    #

    widget.edit_button.click()

    widget.load_research_groups()

    edited = widget._service.get_research_group(
        group_id,
    )

    assert edited is not None

    assert (
        edited.group_name
        == updated_name
    )

    #
    # Restore original value
    #

    edited.group_name = original_name

    widget._service.update_research_group()

    widget.load_research_groups()

def test_delete_research_group(qtbot) -> None:
    """
    Verify a research group can be deleted through the GUI.
    """

    widget = ResearchGroupWidget()

    qtbot.addWidget(widget)

    widget.show()

    #
    # Create temporary research group
    #

    group = ResearchGroup(
        group_name=f"Delete Test {uuid.uuid4()}",
        department_id=1,
        head_lecturer_id=1,
    )

    widget._service.create_research_group(
        group,
    )

    widget.load_research_groups()

    #
    # Locate the research group
    #

    row = None

    for i in range(
        widget.model.rowCount()
    ):

        if (
            widget.model.research_group_at(i).research_group_id
            == group.research_group_id
        ):

            row = i

            break

    assert row is not None

    widget.table.selectRow(
        row,
    )

    qtbot.waitUntil(
        lambda: widget.selected_research_group() is not None,
        timeout=1000,
    )

    #
    # Confirm delete
    #

    def confirm_delete() -> None:

        for window in QApplication.topLevelWidgets():

            if isinstance(
                window,
                QMessageBox,
            ):

                yes_button = window.button(
                    QMessageBox.StandardButton.Yes,
                )

                if yes_button is not None:

                    qtbot.mouseClick(
                        yes_button,
                        Qt.MouseButton.LeftButton,
                    )

                    return

    #
    # Close success dialog
    #

    def close_success() -> None:

        for window in QApplication.topLevelWidgets():

            if isinstance(
                window,
                QMessageBox,
            ):

                ok_button = window.button(
                    QMessageBox.StandardButton.Ok,
                )

                if ok_button is not None:

                    qtbot.mouseClick(
                        ok_button,
                        Qt.MouseButton.LeftButton,
                    )

                    return

    #
    # Schedule helpers
    #

    QTimer.singleShot(
        0,
        confirm_delete,
    )

    QTimer.singleShot(
        500,
        close_success,
    )

    #
    # Delete
    #

    widget.delete_button.click()

    widget.load_research_groups()

    #
    # Verify deletion
    #

    deleted = widget._service.get_research_group(
        group.research_group_id,
    )

    assert deleted is None

def test_search_group_name(qtbot) -> None:
    """
    Verify searching by group name.
    """

    widget = ResearchGroupWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.model.rowCount() > 0

    group = widget.model.research_group_at(0)

    widget.search_edit.setText(
        group.group_name,
    )

    widget.search_research_groups()

    assert widget.model.rowCount() >= 1

    for row in range(
        widget.model.rowCount()
    ):

        found = widget.model.research_group_at(
            row,
        )

        assert (
            group.group_name.lower()
            in found.group_name.lower()
        )

def test_department_filter(qtbot) -> None:
    """
    Verify department filtering.
    """

    widget = ResearchGroupWidget()

    qtbot.addWidget(widget)

    widget.show()

    #
    # Skip if only "All Departments" exists.
    #

    if widget.department_filter.count() < 2:

        return

    widget.department_filter.setCurrentIndex(
        1,
    )

    widget.search_research_groups()

    department_id = (
        widget.department_filter.currentData()
    )

    for row in range(
        widget.model.rowCount()
    ):

        group = widget.model.research_group_at(
            row,
        )

        assert (
            group.department_id
            == department_id
        )

def test_head_lecturer_filter(qtbot) -> None:
    """
    Verify head lecturer filtering.
    """

    widget = ResearchGroupWidget()

    qtbot.addWidget(widget)

    widget.show()

    #
    # Skip if only "All Head Lecturers" exists.
    #

    if widget.head_lecturer_filter.count() < 2:

        return

    widget.head_lecturer_filter.setCurrentIndex(
        1,
    )

    widget.search_research_groups()

    lecturer_id = (
        widget.head_lecturer_filter.currentData()
    )

    for row in range(
        widget.model.rowCount()
    ):

        group = widget.model.research_group_at(
            row,
        )

        assert (
            group.head_lecturer_id
            == lecturer_id
        )

def test_clear_filters(qtbot) -> None:
    """
    Verify clearing filters restores all research groups.
    """

    widget = ResearchGroupWidget()

    qtbot.addWidget(widget)

    widget.show()

    original_count = (
        widget.model.rowCount()
    )

    if widget.department_filter.count() > 1:

        widget.department_filter.setCurrentIndex(
            1,
        )

    widget.search_research_groups()

    widget.clear_button.click()

    assert (
        widget.model.rowCount()
        == original_count
    )