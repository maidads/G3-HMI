from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from battery_monitor import BatteryMonitor

class SensorDetail(QWidget):
    def __init__(self, sensor_name, dashboard_window):
        super().__init__()
        self.dashboard_window = dashboard_window
        self.setWindowTitle(f"{sensor_name} - Details")
        self.showFullScreen()

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#B0E0E6'))
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Top bar with back button
        top_bar = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setFixedSize(80, 30)
        back_btn.setStyleSheet("background-color: white; color: black; font-weight: bold;")
        back_btn.clicked.connect(self.go_back)
        top_bar.addWidget(back_btn)
        top_bar.addStretch()
        layout.addLayout(top_bar)
        
        # Add sensor title
        title = QLabel(sensor_name)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Add info section with water level and battery
        info_section = QHBoxLayout()
        
        # Water level display (placeholder)
        water_widget = QWidget()
        water_layout = QVBoxLayout(water_widget)
        water_title = QLabel("Water Level")
        water_title.setFont(QFont("Arial", 12, QFont.Bold))
        water_title.setAlignment(Qt.AlignCenter)
        water_value = QLabel("75%")
        water_value.setFont(QFont("Arial", 24))
        water_value.setAlignment(Qt.AlignCenter)
        water_layout.addWidget(water_title)
        water_layout.addWidget(water_value)
        
        # Add battery monitor component
        self.battery_monitor = BatteryMonitor()
        self.battery_monitor.set_level(85)  # Default battery level
        
        # Add widgets to info section
        info_section.addWidget(water_widget)
        info_section.addWidget(self.battery_monitor)
        
        layout.addLayout(info_section)
        
        # Add placeholder for historical data chart
        chart_placeholder = QLabel("Water Level History Chart (Coming Soon)")
        chart_placeholder.setStyleSheet("background-color: white; padding: 20px; border-radius: 8px;")
        chart_placeholder.setAlignment(Qt.AlignCenter)
        chart_placeholder.setMinimumHeight(200)
        layout.addWidget(chart_placeholder)
        
        self.setLayout(layout)

    def go_back(self):
        self.dashboard_window.setWindowState(Qt.WindowNoState)
        self.dashboard_window.show()
        self.dashboard_window.showFullScreen()
        self.close()