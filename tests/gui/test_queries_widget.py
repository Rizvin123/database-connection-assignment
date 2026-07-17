"""
Tests for QueriesWidget.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt

from src.gui.widgets.queries_widget import QueriesWidget

def test_queries_widget_creation(
    qtbot,
) -> None:
    """
    Verify the Queries widget can be created.
    """

    widget = QueriesWidget()

    qtbot.addWidget(
        widget,
    )

    widget.show()

    assert widget.isVisible()

    assert widget.query_combo.count() == 5

def test_query_selector_items(
    qtbot,
) -> None:
    """
    Verify all assignment queries are present.
    """

    widget = QueriesWidget()

    qtbot.addWidget(
        widget,
    )

    assert widget.query_combo.count() == 5

    expected = [

        "Query 1 - Students by Course and Lecturer",

        "Query 2 - Final-Year Students Above Average",

        "Query 3 - Students Not Enrolled",

        "Query 4 - Faculty Advisor Details",

        "Query 5 - Lecturer Expertise Search",

    ]

    for index, text in enumerate(expected):

        assert (
            widget.query_combo.itemText(index)
            == text
        )

def test_parameter_population(
    qtbot,
) -> None:
    """
    Verify parameter controls are populated.
    """

    widget = QueriesWidget()

    qtbot.addWidget(
        widget,
    )

    assert widget.course_combo.count() > 0

    assert widget.lecturer_combo.count() > 0

    assert widget.student_combo.count() > 0

    assert widget.semester_combo.count() > 0

    assert widget.academic_year_combo.count() > 0

    assert widget.research_area_combo.count() > 0

def test_query_1(
    qtbot,
) -> None:
    """
    Verify Query 1 executes successfully.
    """

    widget = QueriesWidget()

    qtbot.addWidget(
        widget,
    )

    widget.show()

    #
    # Select Query 1
    #

    widget.query_combo.setCurrentIndex(
        0,
    )

    #
    # Ensure parameter controls are populated
    #

    assert widget.course_combo.count() > 0

    assert widget.lecturer_combo.count() > 0

    assert widget.semester_combo.count() > 0

    assert widget.academic_year_combo.count() > 0

    #
    # Select the first available values
    #

    widget.course_combo.setCurrentIndex(
        0,
    )

    widget.lecturer_combo.setCurrentIndex(
        0,
    )

    widget.semester_combo.setCurrentIndex(
        0,
    )

    widget.academic_year_combo.setCurrentIndex(
        0,
    )

    #
    # Execute the query
    #

    qtbot.mouseClick(
        widget.run_button,
        Qt.MouseButton.LeftButton,
    )

    #
    # Verify results
    #

    assert (
        widget.model.columnCount()
        == 6
    )

    assert (
        "result(s)"
        in widget.status_label.text()
    )

def test_query_2(
    qtbot,
) -> None:
    """
    Verify Query 2 executes successfully.
    """

    widget = QueriesWidget()

    qtbot.addWidget(
        widget,
    )

    widget.show()

    #
    # Select Query 2
    #

    widget.query_combo.setCurrentIndex(
        1,
    )

    #
    # Set the threshold
    #

    widget.average_spin.setValue(
        70,
    )

    #
    # Execute the query
    #

    qtbot.mouseClick(
        widget.run_button,
        Qt.MouseButton.LeftButton,
    )

    #
    # Verify results
    #

    assert (
        widget.model.columnCount()
        == 6
    )

    assert (
        "result(s)"
        in widget.status_label.text()
    )

def test_query_3(
    qtbot,
) -> None:
    """
    Verify Query 3 executes successfully.
    """

    widget = QueriesWidget()

    qtbot.addWidget(
        widget,
    )

    widget.show()

    #
    # Select Query 3
    #

    widget.query_combo.setCurrentIndex(
        2,
    )

    #
    # Select the first available values
    #

    assert widget.semester_combo.count() > 0

    assert widget.academic_year_combo.count() > 0

    widget.semester_combo.setCurrentIndex(
        0,
    )

    widget.academic_year_combo.setCurrentIndex(
        0,
    )

    #
    # Execute the query
    #

    qtbot.mouseClick(
        widget.run_button,
        Qt.MouseButton.LeftButton,
    )

    #
    # Verify results
    #

    assert (
        widget.model.columnCount()
        == 4
    )

    assert (
        "result(s)"
        in widget.status_label.text()
    )

def test_query_4(
    qtbot,
) -> None:
    """
    Verify Query 4 executes successfully.
    """

    widget = QueriesWidget()

    qtbot.addWidget(
        widget,
    )

    widget.show()

    #
    # Select Query 4
    #

    widget.query_combo.setCurrentIndex(
        3,
    )

    #
    # Select the first student
    #

    assert widget.student_combo.count() > 0

    widget.student_combo.setCurrentIndex(
        0,
    )

    #
    # Execute the query
    #

    qtbot.mouseClick(
        widget.run_button,
        Qt.MouseButton.LeftButton,
    )

    #
    # Verify results
    #

    assert (
        widget.model.columnCount()
        == 7
    )

    assert (
        "result(s)"
        in widget.status_label.text()
    )

def test_query_5(
    qtbot,
) -> None:
    """
    Verify Query 5 executes successfully.
    """

    widget = QueriesWidget()

    qtbot.addWidget(
        widget,
    )

    widget.show()

    #
    # Select Query 5
    #

    widget.query_combo.setCurrentIndex(
        4,
    )

    #
    # Select the first research area
    #

    assert widget.research_area_combo.count() > 0

    widget.research_area_combo.setCurrentIndex(
        0,
    )

    #
    # Execute the query
    #

    qtbot.mouseClick(
        widget.run_button,
        Qt.MouseButton.LeftButton,
    )

    #
    # Verify results
    #

    assert (
        widget.model.columnCount()
        == 5
    )

    assert (
        "result(s)"
        in widget.status_label.text()
    )