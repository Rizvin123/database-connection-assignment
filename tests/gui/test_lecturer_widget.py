"""
Tests for LecturerWidget.
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
from src.models.lecturer import Lecturer
from src.gui.dialogs.lecturer_dialog import LecturerDialog
from src.gui.widgets.lecturer_widget import LecturerWidget


def test_widget_loads(qtbot) -> None:
    """
    Verify the Lecturer widget loads.
    """

    widget = LecturerWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.isVisible()

def test_table_populated(qtbot) -> None:
    """
    Verify lecturers are loaded into the table.
    """

    widget = LecturerWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.model.rowCount() > 0

def test_status_label(qtbot) -> None:
    """
    Verify the status label updates.
    """

    widget = LecturerWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert "lecturer" in widget.status_label.text().lower()

def test_add_lecturer(qtbot) -> None:
    """
    Verify a lecturer can be added through the GUI.
    """

    widget = LecturerWidget()

    qtbot.addWidget(widget)

    widget.show()

    initial_rows = widget.model.rowCount()

    #
    # Fill dialog
    #

    email = f"{uuid.uuid4()}@example.com"

    def fill_dialog() -> None:

        dialog = None

        for window in QApplication.topLevelWidgets():

            if isinstance(
                window,
                LecturerDialog,
            ):

                dialog = window

                break

        assert dialog is not None

        dialog.first_name_edit.setText(
            "GUI",
        )

        dialog.last_name_edit.setText(
            "Lecturer",
        )

        dialog.email_edit.setText(
            email,
        )

        dialog.phone_edit.setText(
            "9999999999",
        )

        dialog.department_combo.setCurrentIndex(
            1,
        )

        dialog.course_load_spin.setValue(
            2,
        )

        if dialog.research_group_combo.count() > 1:

            dialog.research_group_combo.setCurrentIndex(
                1,
            )

        dialog.office_room_edit.setText(
            "A-101",
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
    # Close success message
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

    #
    # Reload
    #

    widget.load_lecturers()

    assert (
        widget.model.rowCount()
        == initial_rows + 1
    )

    #
    # Verify lecturer exists
    #

    lecturer = widget._service.find_by_email(
        email,
    )

    assert lecturer is not None

    assert lecturer.first_name == "GUI"

    #
    # Cleanup
    #

    widget._service.delete_lecturer(
        lecturer.lecturer_id,
    )

    widget.load_lecturers()

def test_edit_lecturer(qtbot) -> None:
    """
    Verify a lecturer can be edited through the GUI.
    """

    widget = LecturerWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.model.rowCount() > 0

    #
    # Select first lecturer
    #

    widget.table.selectRow(0)

    qtbot.waitUntil(
        lambda: widget.selected_lecturer() is not None,
        timeout=1000,
    )

    lecturer = widget.selected_lecturer()

    assert lecturer is not None

    lecturer_id = lecturer.lecturer_id

    original_first_name = lecturer.first_name

    updated_first_name = "EditedGUI"

    #
    # Fill dialog
    #

    def fill_dialog() -> None:

        dialog = None

        for window in QApplication.topLevelWidgets():

            if isinstance(
                window,
                LecturerDialog,
            ):

                dialog = window

                break

        assert dialog is not None

        dialog.first_name_edit.clear()

        dialog.first_name_edit.setText(
            updated_first_name,
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
    # Close success message
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

    QTimer.singleShot(
        0,
        fill_dialog,
    )

    QTimer.singleShot(
        500,
        close_message_box,
    )

    widget.edit_button.click()

    widget.load_lecturers()

    edited = widget._service.get_lecturer(
        lecturer_id,
    )

    assert edited is not None

    assert (
        edited.first_name
        == updated_first_name
    )

    #
    # Restore original value
    #

    edited.first_name = original_first_name

    widget._service.update_lecturer()

    widget.load_lecturers()

def test_delete_lecturer(qtbot) -> None:
    """
    Verify a lecturer can be deleted through the GUI.
    """

    widget = LecturerWidget()

    qtbot.addWidget(widget)

    widget.show()

    #
    # Create temporary lecturer
    #

    lecturer = Lecturer(
        first_name="Delete",
        last_name="Test",
        email=f"{uuid.uuid4()}@example.com",
        phone="9999999999",
        department_id=1,
        course_load=2,
        research_group_id=1,
        office_room="Delete Office",
    )

    created = widget._service.create_lecturer(
        lecturer,
    )

    widget.load_lecturers()

    #
    # Locate lecturer
    #

    row = None

    for i in range(
        widget.model.rowCount()
    ):

        if (
            widget.model.lecturer_at(i).lecturer_id
            == created.lecturer_id
        ):

            row = i

            break

    assert row is not None

    widget.table.selectRow(row)

    qtbot.waitUntil(
        lambda: widget.selected_lecturer() is not None,
        timeout=1000,
    )

    #
    # Confirm deletion
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
    # Close success message
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

    QTimer.singleShot(
        0,
        confirm_delete,
    )

    QTimer.singleShot(
        500,
        close_success,
    )

    widget.delete_button.click()

    widget.load_lecturers()

    deleted = widget._service.get_lecturer(
        created.lecturer_id,
    )

    assert deleted is None