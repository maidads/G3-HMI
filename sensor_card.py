# sensor_card.py
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QSizePolicy, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QColor, QCursor
from PyQt5.QtCore import Qt
from sensor_detail import SensorDetail

class SensorCard(QFrame):
    """
    Displays a sensor card with water level info and status.
    Whole card is clickable to open the detail view.
    """
    def __init__(self, title, dashboard, db=None):
        super().__init__()
        self.dashboard = dashboard
        self.title = title
        self.db = db

        self.setFrameShape(QFrame.NoFrame)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedSize(250, 200)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
            QFrame:hover {
                background-color: #f0f8ff;
            }
        """)

        # Add shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)

        # Sensor title
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # Description
        description = ""
        if self.db:
            sensor_data = self.db.get_sensor_data(self.title)
            description = f"Monitors water level in {sensor_data.get('name', 'tank')}" if sensor_data else ""
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #555;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Status and water level
        if self.db:
            sensor_data = self.db.get_sensor_data(self.title)
            settings = self.db.get_settings()

            if sensor_data and settings:
                water_level = sensor_data.get("current_water_level", None)
                if water_level is not None:
                    status_text = "Normal"
                    status_color = "green"
                    critical_threshold = settings.get("critical_threshold", 100.0)
                    warning_threshold = settings.get("warning_threshold", 80.0)

                    if water_level >= critical_threshold:
                        status_text = "Critical"
                        status_color = "red"
                    elif water_level >= warning_threshold:
                        status_text = "Warning"
                        status_color = "orange"

                    status_label = QLabel(f"Status: {status_text}")
                    status_label.setStyleSheet(f"color: {status_color}; font-weight: bold;")
                    layout.addWidget(status_label)

                    level_label = QLabel(f"Water Level: {water_level:.1f}%")
                    layout.addWidget(level_label)
                else:
                    layout.addWidget(QLabel("Water Level: N/A"))
            else:
                no_data = QLabel("Status: Data Unavailable")
                no_data.setStyleSheet("color: gray; font-style: italic;")
                layout.addWidget(no_data)

        layout.addStretch()

    def mousePressEvent(self, event):
        """Open detail view on click"""
        self.dashboard.hide()
        self.detail_window = SensorDetail(self.title, self.dashboard, self.db)
        self.detail_window.show()
