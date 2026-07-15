"""
Tests for CourseWidget.
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
from src.models.course import Course
from src.gui.dialogs.course_dialog import CourseDialog
from src.gui.widgets.course_widget import CourseWidget

def test_widget_loads(qtbot) -> None:
    """
    Verify the Course widget loads.
    """

    widget = CourseWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.isVisible()

def test_table_populated(qtbot) -> None:
    """
    Verify the table is populated.
    """

    widget = CourseWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.model.rowCount() > 0

def test_status_label(qtbot) -> None:
    """
    Verify the status label.
    """

    widget = CourseWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert "course" in widget.status_label.text().lower()

def test_add_course(qtbot) -> None:
    """
    Verify a course can be added through the GUI.
    """

    widget = CourseWidget()

    qtbot.addWidget(widget)

    widget.show()

    initial_rows = widget.model.rowCount()

    course_code = f"TEST{uuid.uuid4().hex[:8]}"

    #
    # Fill dialog
    #

    def fill_dialog() -> None:

        dialog = None

        for window in QApplication.topLevelWidgets():

            if isinstance(window, CourseDialog):

                dialog = window

                break

        assert dialog is not None

        dialog.course_code_edit.setText(
            course_code,
        )

        dialog.course_name_edit.setText(
            "GUI Test Course",
        )

        dialog.description_edit.setPlainText(
            "Created from GUI test.",
        )

        dialog.department_combo.setCurrentIndex(
            1,
        )

        dialog.level_spin.setValue(
            2,
        )

        dialog.credits_spin.setValue(
            20,
        )

        dialog.schedule_edit.setText(
            "Friday 10:00",
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

    widget.add_button.click()

    widget.load_courses()

    assert (
        widget.model.rowCount()
        == initial_rows + 1
    )

    course = widget._service.get_course(
        course_code,
    )

    assert course is not None

    assert (
        course.course_name
        == "GUI Test Course"
    )

    #
    # Cleanup
    #

    widget._service.delete_course(
        course_code,
    )

    widget.load_courses()

def test_edit_course(qtbot) -> None:
    """
    Verify a course can be edited through the GUI.
    """

    widget = CourseWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.model.rowCount() > 0

    #
    # Select first row
    #

    widget.table.selectRow(0)

    qtbot.waitUntil(
        lambda: widget.selected_course() is not None,
        timeout=1000,
    )

    course = widget.selected_course()

    assert course is not None

    course_code = course.course_code

    original_name = course.course_name

    updated_name = "Edited GUI Course"

    #
    # Fill dialog
    #

    def fill_dialog() -> None:

        dialog = None

        for window in QApplication.topLevelWidgets():

            if isinstance(window, CourseDialog):

                dialog = window

                break

        assert dialog is not None

        dialog.course_name_edit.clear()

        dialog.course_name_edit.setText(
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
    # Close success message
    #

    def close_message_box() -> None:

        for window in QApplication.topLevelWidgets():

            if isinstance(window, QMessageBox):

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

    #
    # Reload
    #

    widget.load_courses()

    edited = widget._service.get_course(
        course_code,
    )

    assert edited is not None

    assert edited.course_name == updated_name

    #
    # Restore original value
    #

    edited.course_name = original_name

    widget._service.update_course()

    widget.load_courses()

def test_delete_course(qtbot) -> None:
    """
    Verify a course can be deleted through the GUI.
    """

    widget = CourseWidget()

    qtbot.addWidget(widget)

    widget.show()

    #
    # Create temporary course
    #

    course_code = f"TEST{uuid.uuid4().hex[:8]}"

    course = Course(
        course_code=course_code,
        course_name="Delete Test Course",
        description="Temporary course",
        department_id=1,
        level=2,
        credits=15,
        schedule="Monday 09:00",
    )

    widget._service.create_course(course)

    widget.load_courses()

    #
    # Locate the course
    #

    row = None

    for i in range(widget.model.rowCount()):

        if (
            widget.model.course_at(i).course_code
            == course_code
        ):

            row = i

            break

    assert row is not None

    widget.table.selectRow(row)

    qtbot.waitUntil(
        lambda: widget.selected_course() is not None,
        timeout=1000,
    )

    #
    # Confirm delete dialog
    #

    def confirm_delete() -> None:

        for window in QApplication.topLevelWidgets():

            if isinstance(window, QMessageBox):

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

            if isinstance(window, QMessageBox):

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

    widget.load_courses()

    #
    # Verify
    #

    deleted = widget._service.get_course(
        course_code,
    )

    assert deleted is None