# .\dashboard.py
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QScrollArea, QPushButton, QHBoxLayout)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSlot
from sensor_card import SensorCard
from settings_screen import SettingsScreen

class Dashboard(QWidget):
    """
    Main screen displaying all sensors and access to settings.
    """
    def __init__(self):
        super().__init__()
        self.settings_screen = None
        self.init_ui()

    def init_ui(self):
        """Sets up the dashboard UI"""
        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#B0E0E6'))  # Light blue
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and settings button
        header_layout = QHBoxLayout()
        title = QLabel("Water Level Monitor")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color: black;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        settings_btn = QPushButton("Settings")
        settings_btn.setFixedSize(100, 30)
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: white; 
                color: black;
                border: none; 
                border-radius: 5px;
                padding: 5px; 
                font-weight: bold;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """)
        settings_btn.clicked.connect(self.open_settings)
        header_layout.addWidget(settings_btn)
        main_layout.addLayout(header_layout)

        # Subheader
        subheader = QLabel("Click 'Go to Details' to view sensor information")
        subheader.setStyleSheet("color: #333; margin-bottom: 10px;")
        main_layout.addWidget(subheader)

        # Scrollable area for sensor cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background-color: transparent; 
            }
            QWidget#scrollContainer { 
                background-color: transparent; 
            }
        """)

        scroll_content_widget = QWidget()
        scroll_content_widget.setObjectName("scrollContainer")
        scroll_content_widget.setStyleSheet("background-color: transparent;")

        # Layout for sensor cards - center them horizontally
        sensor_layout = QVBoxLayout(scroll_content_widget)
        sensor_layout.setAlignment(Qt.AlignHCenter)
        sensor_layout.setSpacing(20)
        sensor_layout.setContentsMargins(10, 10, 10, 10)

        # Add sensor cards
        sensor_layout.addWidget(SensorCard("Sensor 1", "Monitors water level in main tank", self))
        sensor_layout.addWidget(SensorCard("Sensor 2", "Monitors water level in reserve tank", self))
        sensor_layout.addWidget(SensorCard("Sensor 3", "Monitors water level in overflow tank", self))

        scroll_area.setWidget(scroll_content_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def open_settings(self):
        """Opens the settings screen"""
        if self.settings_screen is None or not self.settings_screen.isVisible():
            self.settings_screen = SettingsScreen(parent=self)
            self.settings_screen.closed.connect(self.show_dashboard)

            self.hide()
            self.settings_screen.setWindowFlags(Qt.Window)
            self.settings_screen.showFullScreen()

    @pyqtSlot()
    def show_dashboard(self):
        """Shows the dashboard when returning from settings"""
        self.showFullScreen()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.showFullScreen()
    sys.exit(app.exec_())