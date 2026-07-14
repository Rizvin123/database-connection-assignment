"""
Main application window.
"""

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QListWidget
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QSplitter
from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtWidgets import QStatusBar
from PyQt6.QtWidgets import QLabel

from src.gui.widgets.dashboard_widget import DashboardWidget
from src.gui.widgets.student_widget import StudentWidget
from src.gui.widgets.lecturer_widget import LecturerWidget



class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(
            "University Records Management System"
        )

        self.resize(1200, 800)

        splitter = QSplitter()

        self.navigation = QListWidget()

        self.navigation.addItems(
            [
                "Dashboard",
                "Students",
                "Lecturers",
                "Courses",
                "Staff",
                "Research",
                "Queries",
            ]
        )

        self.navigation.setFixedWidth(220)

        self.pages = QStackedWidget()

        self.dashboard_page = DashboardWidget()
        self.student_page = StudentWidget()
        self.lecturer_page = LecturerWidget()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.student_page)
        self.pages.addWidget(self.lecturer_page)

        splitter.addWidget(self.navigation)
        splitter.addWidget(self.pages)

        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)

        status = QStatusBar()

        status.showMessage("Ready")

        self.setStatusBar(status)

        self.navigation.currentRowChanged.connect(
            self.change_page
        )

        self.navigation.setCurrentRow(0)     

        self.pages.addWidget(QLabel("Courses - Coming Soon"))
        self.pages.addWidget(QLabel("Staff - Coming Soon"))
        self.pages.addWidget(QLabel("Research - Coming Soon"))
        self.pages.addWidget(QLabel("Queries - Coming Soon"))

    def change_page(
        self,
        index: int,
    ) -> None:
        """
        Switch between application pages.
        """

        if index < self.pages.count():
            self.pages.setCurrentIndex(index)