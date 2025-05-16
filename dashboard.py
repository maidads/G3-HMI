# dashboard.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QScrollArea, QPushButton, QHBoxLayout, QGridLayout, QFrame
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSlot
from sensor_card import SensorCard
from settings_screen import SettingsScreen
from database_connector import DatabaseConnector
from PyQt5.QtGui import QFont, QCursor



class Dashboard(QWidget):
    """
    Main screen displaying all sensors and access to settings.
    """
    def __init__(self):
        super().__init__()
        self.settings_screen = None
        self.db = DatabaseConnector.get_instance()
        self.init_ui()

    def init_ui(self):
        # Set background
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#B0E0E6'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
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
        subheader = QLabel("Click a sensor card to view details")
        subheader.setStyleSheet("color: #333; margin-bottom: 10px;")
        main_layout.addWidget(subheader)

        # Scroll area
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

        # Grid: 3 rows x 4 columns
        grid_layout = QGridLayout(scroll_content_widget)
        grid_layout.setSpacing(20)
        grid_layout.setContentsMargins(10, 10, 10, 10)

        sensor_ids = self.db.get_sensors()
        total_cards = 12
        sensors_to_display = sensor_ids[:total_cards]  # max 12

        # Fyll med None för tomma slotar
        while len(sensors_to_display) < total_cards:
            sensors_to_display.append(None)

        for i in range(total_cards):
            row = i // 4
            col = i % 4
            sensor_id = sensors_to_display[i]

            if sensor_id:
                card = SensorCard(sensor_id, self, db=self.db)
            else:
                card = self.create_empty_slot()

            grid_layout.addWidget(card, row, col)

        scroll_area.setWidget(scroll_content_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def create_empty_slot(self):
        """Create a clickable slot to add a new sensor"""
        frame = QFrame()
        frame.setFixedSize(250, 200)
        frame.setCursor(QCursor(Qt.PointingHandCursor))
        frame.setStyleSheet("""
            QFrame {
                background-color: #eeeeee;
                border-radius: 12px;
                border: 1px dashed #bbb;
            }
            QFrame:hover {
                background-color: #e0f7fa;
            }
        """)

        label = QLabel("➕ Add Sensor", frame)
        label.setFont(QFont("Arial", 12, QFont.StyleItalic))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #666;")

        layout = QVBoxLayout(frame)
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()

        # Gör hela rutan klickbar
        def open_add_sensor():
            self.open_settings()  # eller visa separat dialog

        frame.mousePressEvent = lambda event: open_add_sensor()

        return frame

    def open_settings(self):
        if self.settings_screen is None or not self.settings_screen.isVisible():
            self.settings_screen = SettingsScreen(parent=self, db=self.db)
            self.settings_screen.closed.connect(self.show_dashboard)
            self.hide()
            self.settings_screen.setWindowFlags(Qt.Window)
            self.settings_screen.showFullScreen()

    @pyqtSlot()
    def show_dashboard(self):
        self.showFullScreen()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.showFullScreen()
    sys.exit(app.exec_())
