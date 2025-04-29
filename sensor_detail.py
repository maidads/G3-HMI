# .\sensor_detail.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from battery_monitor import BatteryMonitor
from water_level_chart import WaterLevelChart
from alarm_system import AlarmSystem

class SensorDetail(QWidget):
    """
    Detailed view of a single sensor showing current readings,
    alarm status, battery level, and historical data.
    """
    def __init__(self, sensor_name, dashboard_window):
        super().__init__()
        self.dashboard_window = dashboard_window
        self.sensor_name = sensor_name

        self.setWindowTitle(f"{sensor_name} - Details")
        self.showFullScreen()

        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#B0E0E6'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Back button
        top_bar_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setFixedSize(80, 30)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: white; color: black;
                border: 1px solid #ccc; border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """)
        back_btn.clicked.connect(self.go_back)
        top_bar_layout.addWidget(back_btn, alignment=Qt.AlignLeft)
        top_bar_layout.addStretch()
        main_layout.addLayout(top_bar_layout)

        # Sensor title
        title = QLabel(sensor_name)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Alarm system
        alarm_label = QLabel("Alarm Status")
        alarm_label.setFont(QFont("Arial", 14, QFont.Bold))
        alarm_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(alarm_label)
        
        self.alarm_system = AlarmSystem()
        main_layout.addWidget(self.alarm_system)

        # Current readings section (water level & battery)
        info_section_layout = QHBoxLayout()
        
        # Water level display
        water_container = QFrame()
        water_container.setFrameShape(QFrame.NoFrame)
        water_container.setFixedWidth(200)
        
        water_layout = QVBoxLayout(water_container)
        water_title = QLabel("Current Water Level")
        water_title.setFont(QFont("Arial", 12, QFont.Bold))
        water_title.setAlignment(Qt.AlignCenter)
        
        # Placeholder value - would be replaced with actual sensor data
        current_water_level = 65
        self.water_value = QLabel(f"{current_water_level}%")
        self.water_value.setFont(QFont("Arial", 28, QFont.Bold))
        self.water_value.setAlignment(Qt.AlignCenter)
        water_layout.addWidget(water_title)
        water_layout.addWidget(self.water_value)
        
        # Battery display container
        battery_container = QFrame()
        battery_container.setFrameShape(QFrame.NoFrame)
        battery_container.setFixedWidth(350)
        
        battery_layout = QVBoxLayout(battery_container)
        battery_title = QLabel("Battery")
        battery_title.setFont(QFont("Arial", 12, QFont.Bold))
        battery_title.setAlignment(Qt.AlignCenter)
        battery_layout.addWidget(battery_title)
        
        # Add battery monitor
        self.battery_monitor = BatteryMonitor()
        self.battery_monitor.set_level(85)  # Placeholder level
        battery_layout.addWidget(self.battery_monitor)
        
        info_section_layout.addWidget(water_container)
        info_section_layout.addWidget(battery_container)
        
        main_layout.addLayout(info_section_layout)

        # History chart
        chart_label = QLabel("Water Level History (Last 7 Days)")
        chart_label.setFont(QFont("Arial", 14, QFont.Bold))
        chart_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(chart_label)

        # Try to extract sensor ID for chart data
        sensor_id_for_chart = None
        if sensor_name:
            parts = sensor_name.split()
            if parts and parts[-1].isdigit():
                try:
                    sensor_id_for_chart = int(parts[-1])
                except ValueError:
                    pass

        self.water_chart = WaterLevelChart()
        self.water_chart.update_chart(sensor_id_for_chart)
        self.water_chart.setMinimumHeight(300)
        main_layout.addWidget(self.water_chart)

        main_layout.addStretch()

        # Check alarm with current water level
        self.alarm_system.check_water_level(self.sensor_name, current_water_level)

    def go_back(self):
        """Returns to the dashboard view"""
        self.dashboard_window.showFullScreen()
        self.close()