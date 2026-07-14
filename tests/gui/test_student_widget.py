"""
End-to-end tests for StudentWidget.
"""

from __future__ import annotations

import uuid

from datetime import date
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLineEdit,
    QMessageBox,
)

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer

from PyQt6.QtWidgets import (
    QApplication,
)

from src.gui.dialogs.student_dialog import StudentDialog
from src.gui.widgets.student_widget import StudentWidget
from src.models.student import Student

def test_widget_loads_students(qtbot) -> None:
    """
    Verify that the StudentWidget loads successfully.
    """

    widget = StudentWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.isVisible()

    assert widget.table.model() is not None

def test_table_contains_students(qtbot) -> None:
    """
    Verify that students are loaded into the table.
    """

    widget = StudentWidget()

    qtbot.addWidget(widget)

    widget.show()

    qtbot.waitUntil(
        lambda: widget.model.rowCount() >= 0,
        timeout=3000,
    )

    assert widget.model.rowCount() > 0

def test_status_label_matches_table(qtbot) -> None:
    """
    Verify that the status label reflects the number of students.
    """

    widget = StudentWidget()

    qtbot.addWidget(widget)

    widget.show()

    count = widget.model.rowCount()

    assert widget.status_label.text() == f"{count} student(s)"

def test_add_student(qtbot) -> None:
    """
    Verify a student can be added through the GUI.
    """

    widget = StudentWidget()

    qtbot.addWidget(widget)

    widget.show()

    initial_rows = widget.model.rowCount()

    email = f"{uuid.uuid4()}@example.com"

    def fill_dialog() -> None:

        dialog = None

        for window in QApplication.topLevelWidgets():

            if isinstance(window, StudentDialog):

                dialog = window

                break

        assert dialog is not None

        dialog.first_name_edit.setText("GUI")

        dialog.last_name_edit.setText("Test")

        dialog.email_edit.setText(email)

        dialog.phone_edit.setText("9999999999")

        dialog.address_edit.setText("GUI Test Address")

        dialog.year_spin.setValue(2)

        buttons = dialog.findChild(QDialogButtonBox)

        save_button = buttons.button(
            QDialogButtonBox.StandardButton.Save
        )

        qtbot.mouseClick(
            save_button,
            Qt.MouseButton.LeftButton,
        )

    def close_message_box() -> None:
        """
        Close the success message box.
        """

        for window in QApplication.topLevelWidgets():
            if isinstance(window, QMessageBox):

                ok_button = window.button(
                    QMessageBox.StandardButton.Ok
                )

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

    qtbot.waitUntil(
        lambda: widget.model.rowCount() == initial_rows + 1,
        timeout=5000,
    )

    assert widget.model.rowCount() == initial_rows + 1

    added_student = None

    for row in range(widget.model.rowCount()):

        student = widget.model.student_at(row)

        if student.email == email:

            added_student = student

            break

    assert added_student is not None

    widget._service.delete_student(
        added_student.student_id,
    )

    widget.load_students()

def test_edit_student(qtbot) -> None:
    """
    Verify a student can be edited through the GUI.
    """

    widget = StudentWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.model.rowCount() > 0

    #
    # Select the first student
    #

    widget.table.selectRow(0)

    qtbot.waitUntil(
        lambda: widget.selected_student() is not None,
        timeout=1000,
    )

    student = widget.selected_student()

    assert student is not None

    student_id = student.student_id

    original_first_name = student.first_name

    updated_first_name = "EditedGUI"

    #
    # Fill the Edit dialog
    #

    def fill_dialog() -> None:

        dialog = None

        for window in QApplication.topLevelWidgets():

            if isinstance(window, StudentDialog):

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

        assert buttons is not None

        save_button = buttons.button(
            QDialogButtonBox.StandardButton.Save,
        )

        qtbot.mouseClick(
            save_button,
            Qt.MouseButton.LeftButton,
        )

    #
    # Close the success message
    #

    def close_message_box() -> None:

        for window in QApplication.topLevelWidgets():

            if isinstance(window, QMessageBox):

                ok_button = window.button(
                    QMessageBox.StandardButton.Ok,
                )

                qtbot.mouseClick(
                    ok_button,
                    Qt.MouseButton.LeftButton,
                )

                return

    #
    # Schedule dialog automation
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
    # Open the Edit dialog
    #

    widget.edit_button.click()

    #
    # Reload the table
    #

    widget.load_students()

    #
    # Verify using the database record,
    # not the table row.
    #

    edited_student = widget._service.get_student(
        student_id,
    )

    assert edited_student is not None

    assert (
        edited_student.first_name
        == updated_first_name
    )

    #
    # Restore the original value
    #

    edited_student.first_name = original_first_name

    widget._service.update_student()

    widget.load_students()

    restored_student = widget._service.get_student(
        student_id,
    )

    assert restored_student is not None

    assert (
        restored_student.first_name
        == original_first_name
    )

def test_delete_student(qtbot) -> None:
    """
    Verify a student can be deleted through the GUI.
    """

    widget = StudentWidget()

    qtbot.addWidget(widget)

    widget.show()

    #
    # Create a temporary student
    #

    student = Student(
        first_name="Delete",
        last_name="Test",
        date_of_birth=date(2000, 1, 1),
        email=f"{uuid.uuid4()}@example.com",
        phone="9999999999",
        address="Delete Test",
        program_id=1,
        year_of_study=1,
        graduation_status="Not Graduated",
        advisor_lecturer_id=1,
    )

    created = widget._service.create_student(student)

    widget.load_students()

    #
    # Locate the student in the table
    #

    row = None

    for i in range(widget.model.rowCount()):

        if widget.model.student_at(i).student_id == created.student_id:

            row = i

            break

    assert row is not None

    widget.table.selectRow(row)

    qtbot.waitUntil(
        lambda: widget.selected_student() is not None,
        timeout=1000,
    )

    #
    # Automatically answer Yes
    #

    def confirm_delete() -> None:

        for window in QApplication.topLevelWidgets():

            if isinstance(window, QMessageBox):

                yes_button = window.button(
                    QMessageBox.StandardButton.Yes
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

            if isinstance(window, QMessageBox):

                ok_button = window.button(
                    QMessageBox.StandardButton.Ok
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

    widget.load_students()

    #
    # Verify student no longer exists
    #

    deleted = widget._service.get_student(
        created.student_id,
    )

    assert deleted is None

def test_search_students(qtbot) -> None:
    """
    Verify searching students through the GUI.
    """

    widget = StudentWidget()

    qtbot.addWidget(widget)

    widget.show()

    initial_count = widget.model.rowCount()

    assert initial_count > 0

    widget.search_field_combo.setCurrentText(
        "First Name",
    )

    widget.search_edit.setText(
        "Alice",
    )

    qtbot.keyClick(
        widget.search_edit,
        Qt.Key.Key_Return,
    )

    qtbot.waitUntil(
        lambda: widget.model.rowCount() > 0,
        timeout=3000,
    )

    for row in range(widget.model.rowCount()):

        student = widget.model.student_at(row)

        assert "alice" in student.first_name.lower()

def test_filter_by_program(qtbot) -> None:
    """
    Verify filtering students by program.
    """

    widget = StudentWidget()

    qtbot.addWidget(widget)

    widget.show()

    if widget.program_filter.count() < 2:
        return

    widget.program_filter.setCurrentIndex(1)

    qtbot.wait(500)

    program_id = widget.program_filter.currentData()

    for row in range(widget.model.rowCount()):

        student = widget.model.student_at(row)

        assert student.program_id == program_id

def test_filter_by_year(qtbot) -> None:
    """
    Verify filtering students by year.
    """

    widget = StudentWidget()

    qtbot.addWidget(widget)

    widget.show()

    widget.year_filter.setCurrentText("1")

    qtbot.wait(500)

    for row in range(widget.model.rowCount()):

        student = widget.model.student_at(row)

        assert student.year_of_study == 1

def test_filter_by_status(qtbot) -> None:
    """
    Verify filtering students by graduation status.
    """

    widget = StudentWidget()

    qtbot.addWidget(widget)

    widget.show()

    widget.status_filter.setCurrentText(
        "Graduated",
    )

    qtbot.wait(500)

    for row in range(widget.model.rowCount()):

        student = widget.model.student_at(row)

        assert (
            student.graduation_status
            == "Graduated"
        )

def test_clear_filters(qtbot) -> None:
    """
    Verify clearing search filters.
    """

    widget = StudentWidget()

    qtbot.addWidget(widget)

    widget.show()

    total = widget.model.rowCount()

    widget.search_edit.setText("Alice")

    qtbot.keyClick(
        widget.search_edit,
        Qt.Key.Key_Return,
    )

    qtbot.wait(500)

    widget.clear_button.click()

    qtbot.waitUntil(
        lambda: widget.model.rowCount() == total,
        timeout=3000,
    )

    assert widget.search_edit.text() == ""

    assert widget.search_field_combo.currentIndex() == 0

    assert widget.program_filter.currentIndex() == 0

    assert widget.year_filter.currentIndex() == 0

    assert widget.status_filter.currentIndex() == 0