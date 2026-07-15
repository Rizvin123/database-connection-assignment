"""
GUI tests for StaffWidget.
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
from src.models.staff import Staff
from src.gui.dialogs.staff_dialog import StaffDialog
from src.gui.widgets.staff_widget import StaffWidget


def test_widget_loads(qtbot) -> None:
    """
    Verify the Staff widget loads successfully.
    """

    widget = StaffWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.isVisible()


def test_table_populated(qtbot) -> None:
    """
    Verify the staff table is populated.
    """

    widget = StaffWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.model.rowCount() > 0


def test_status_label(qtbot) -> None:
    """
    Verify the status label displays the number of staff members.
    """

    widget = StaffWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert "staff" in widget.status_label.text().lower()

def test_add_staff(qtbot) -> None:
    """
    Verify a staff member can be added through the GUI.
    """

    widget = StaffWidget()

    qtbot.addWidget(widget)

    widget.show()

    initial_rows = widget.model.rowCount()

    email = f"{uuid.uuid4()}@example.com"

    #
    # Fill dialog
    #

    def fill_dialog() -> None:

        dialog = None

        for window in QApplication.topLevelWidgets():

            if isinstance(window, StaffDialog):

                dialog = window

                break

        assert dialog is not None

        dialog.first_name_edit.setText(
            "GUI",
        )

        dialog.last_name_edit.setText(
            "Tester",
        )

        dialog.email_edit.setText(
            email,
        )

        dialog.phone_edit.setText(
            "9999999999",
        )

        dialog.job_title_edit.setText(
            "GUI Administrator",
        )

        dialog.department_combo.setCurrentIndex(
            1,
        )

        dialog.employment_type_combo.setCurrentText(
            "Full-Time",
        )

        dialog.contract_details_edit.setPlainText(
            "Permanent Employee",
        )

        dialog.salary_spin.setValue(
            60000,
        )

        dialog.emergency_contact_name_edit.setText(
            "Emergency Contact",
        )

        dialog.emergency_contact_phone_edit.setText(
            "8888888888",
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

    widget.load_staff()

    assert (
        widget.model.rowCount()
        == initial_rows + 1
    )

    staff = widget._service.find_by_email(
        email,
    )

    assert staff is not None

    assert (
        staff.job_title
        == "GUI Administrator"
    )

    #
    # Cleanup
    #

    widget._service.delete_staff(
        staff.staff_id,
    )

    widget.load_staff()

def test_edit_staff(qtbot) -> None:
    """
    Verify a staff member can be edited through the GUI.
    """

    widget = StaffWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.model.rowCount() > 0

    #
    # Select first row
    #

    widget.table.selectRow(0)

    qtbot.waitUntil(
        lambda: widget.selected_staff() is not None,
        timeout=1000,
    )

    staff = widget.selected_staff()

    assert staff is not None

    staff_id = staff.staff_id

    original_first_name = staff.first_name

    updated_first_name = "EditedGUI"

    #
    # Fill dialog
    #

    def fill_dialog() -> None:

        dialog = None

        for window in QApplication.topLevelWidgets():

            if isinstance(
                window,
                StaffDialog,
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

    widget.load_staff()

    edited = widget._service.get_staff(
        staff_id,
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

    widget._service.update_staff()

    widget.load_staff()

def test_delete_staff(qtbot) -> None:
    """
    Verify a staff member can be deleted through the GUI.
    """

    widget = StaffWidget()

    qtbot.addWidget(widget)

    widget.show()

    #
    # Create temporary staff member
    #

    staff = Staff(
        first_name="Delete",
        last_name="Test",
        email=f"{uuid.uuid4()}@example.com",
        phone="9999999999",
        job_title="Delete Tester",
        department_id=1,
        employment_type="Full-Time",
        contract_details="Temporary record",
        salary=50000,
        emergency_contact_name="Emergency",
        emergency_contact_phone="8888888888",
    )

    widget._service.create_staff(
        staff,
    )

    widget.load_staff()

    #
    # Locate the staff member
    #

    row = None

    for i in range(
        widget.model.rowCount()
    ):

        if (
            widget.model.staff_at(i).staff_id
            == staff.staff_id
        ):

            row = i

            break

    assert row is not None

    widget.table.selectRow(
        row,
    )

    qtbot.waitUntil(
        lambda: widget.selected_staff() is not None,
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

    widget.load_staff()

    #
    # Verify deletion
    #

    deleted = widget._service.get_staff(
        staff.staff_id,
    )

    assert deleted is None

def test_search_first_name(qtbot) -> None:
    """
    Verify searching by first name.
    """

    widget = StaffWidget()

    qtbot.addWidget(widget)

    widget.show()

    #
    # Use an existing staff member
    #

    assert widget.model.rowCount() > 0

    staff = widget.model.staff_at(0)

    index = widget.search_field_combo.findData(
    "first_name",
    )

    widget.search_field_combo.setCurrentIndex(
        index,
    )

    widget.search_edit.setText(
        staff.first_name,
    )

    widget.search_staff()

    assert widget.model.rowCount() >= 1

    for row in range(
        widget.model.rowCount()
    ):

        found = widget.model.staff_at(
            row,
        )

        assert (
            staff.first_name.lower()
            in found.first_name.lower()
        )

def test_search_last_name(qtbot) -> None:
    """
    Verify searching by last name.
    """

    widget = StaffWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.model.rowCount() > 0

    staff = widget.model.staff_at(0)

    index = widget.search_field_combo.findData(
        "last_name",
    )

    widget.search_field_combo.setCurrentIndex(
        index,
    )

    widget.search_edit.setText(
        staff.last_name,
    )

    widget.search_staff()

    assert widget.model.rowCount() >= 1

    for row in range(
        widget.model.rowCount()
    ):

        found = widget.model.staff_at(
            row,
        )

        assert (
            staff.last_name.lower()
            in found.last_name.lower()
        )

def test_search_email(qtbot) -> None:
    """
    Verify searching by email.
    """

    widget = StaffWidget()

    qtbot.addWidget(widget)

    widget.show()

    assert widget.model.rowCount() > 0

    staff = widget.model.staff_at(0)

    index = widget.search_field_combo.findData(
        "email",
    )

    widget.search_field_combo.setCurrentIndex(
        index,
    )

    widget.search_edit.setText(
        staff.email,
    )

    widget.search_staff()

    assert widget.model.rowCount() == 1

    found = widget.model.staff_at(0)

    assert found.email == staff.email

def test_department_filter(qtbot) -> None:
    """
    Verify department filtering.
    """

    widget = StaffWidget()

    qtbot.addWidget(widget)

    widget.show()

    #
    # Skip if only "All Departments" exists
    #

    if widget.department_filter.count() < 2:

        return

    widget.department_filter.setCurrentIndex(1)

    widget.search_staff()

    department_id = (
        widget.department_filter.currentData()
    )

    for row in range(
        widget.model.rowCount()
    ):

        staff = widget.model.staff_at(row)

        assert (
            staff.department_id
            == department_id
        )

def test_job_title_filter(qtbot) -> None:
    """
    Verify job title filtering.
    """

    widget = StaffWidget()

    qtbot.addWidget(widget)

    widget.show()

    #
    # Skip if only "All Job Titles" exists
    #

    if widget.job_title_filter.count() < 2:

        return

    widget.job_title_filter.setCurrentIndex(1)

    widget.search_staff()

    job_title = (
        widget.job_title_filter.currentData()
    )

    for row in range(
        widget.model.rowCount()
    ):

        staff = widget.model.staff_at(row)

        assert (
            staff.job_title
            == job_title
        )

def test_clear_filters(qtbot) -> None:
    """
    Verify clearing filters restores all staff.
    """

    widget = StaffWidget()

    qtbot.addWidget(widget)

    widget.show()

    original_count = widget.model.rowCount()

    if widget.department_filter.count() > 1:

        widget.department_filter.setCurrentIndex(
            1,
        )

    widget.search_staff()

    widget.clear_button.click()

    assert (
        widget.model.rowCount()
        == original_count
    )