"""
Dashboard widget.
"""

from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


class DashboardWidget(QWidget):
    """
    Dashboard page displayed when the application starts.
    """

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("University Records Management System")
        title.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            """
        )

        welcome = QLabel(
            "Welcome.\n\n"
            "Select a module from the navigation menu."
        )

        layout.addWidget(title)
        layout.addWidget(welcome)
        layout.addStretch()