# .\alarm_system.py
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QMainWindow, QSlider, QCheckBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

class AlarmSystem(QWidget):
    """
    Displays alarm status for water levels with color-coded indicators.
    Changes from green (Normal) to orange (Warning) to red (Critical).
    """

    # Signals for other components to react to alarm state changes
    alarm_triggered = pyqtSignal(str, str)  # (sensor_id, message)
    alarm_cleared = pyqtSignal(str)         # (sensor_id)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Default thresholds (configurable)
        self.warning_threshold = 75
        self.critical_threshold = 85
        self.alarm_state = "Normal"
        
        self.init_ui()
        
        # For demo/testing mode
        self.demo_mode = False
        self.demo_timer = QTimer(self)
        self.demo_timer.timeout.connect(self.cycle_demo_states)

    def init_ui(self):
        """Creates the alarm status display"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 5)

        # Status indicator with color background
        self.status_frame = QFrame()
        self.status_frame.setFrameShape(QFrame.StyledPanel)
        self.status_frame.setLineWidth(0)
        self.status_frame.setStyleSheet("background-color: green; border-radius: 8px;")
        self.status_frame.setMinimumHeight(40)

        # Status text
        status_layout = QVBoxLayout(self.status_frame)
        self.status_label = QLabel("Normal")
        self.status_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: white;")
        status_layout.addWidget(self.status_label)

        # Message below status indicator
        self.message_label = QLabel("Water level within safe limits")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 10pt;")

        layout.addWidget(self.status_frame)
        layout.addWidget(self.message_label)

    def check_water_level(self, sensor_id, water_level):
        """Updates alarm state based on water level"""
        old_state = self.alarm_state

        # Ensure water_level is treated as a float for comparison and formatting
        try:
            level = float(water_level)
        except (ValueError, TypeError):
             # Handle cases where water_level might not be a number
             self.set_warning_alarm(f"Invalid level data received: {water_level}")
             print(f"Warning: Invalid water level data for {sensor_id}: {water_level}")
             return # Stop processing if data is invalid

        if level >= self.critical_threshold:
            # --- FORMATTING APPLIED HERE ---
            self.set_critical_alarm(f"CRITICAL: Water level at {level:.2f}%")
            if old_state != "Critical":
                self.alarm_triggered.emit(sensor_id, f"Critical water level: {level:.2f}%")
        elif level >= self.warning_threshold:
            # --- FORMATTING APPLIED HERE ---
            self.set_warning_alarm(f"WARNING: Water level at {level:.2f}%")
            if old_state != "Warning":
                self.alarm_triggered.emit(sensor_id, f"Warning water level: {level:.2f}%")
        else:
            # No need to display the level in the 'Normal' message typically
            self.clear_alarm("Water level within safe limits")
            if old_state != "Normal":
                self.alarm_cleared.emit(sensor_id)

    def set_warning_alarm(self, message):
        """Sets alarm to Warning state (orange)"""
        self.alarm_state = "Warning"
        self.status_frame.setStyleSheet("background-color: orange; border-radius: 8px;")
        self.status_label.setText("Warning")
        self.message_label.setText(message)

    def set_critical_alarm(self, message):
        """Sets alarm to Critical state (red)"""
        self.alarm_state = "Critical"
        self.status_frame.setStyleSheet("background-color: red; border-radius: 8px;")
        self.status_label.setText("Critical")
        self.message_label.setText(message)

    def clear_alarm(self, message="Normal operation"):
        """Sets alarm to Normal state (green)"""
        self.alarm_state = "Normal"
        self.status_frame.setStyleSheet("background-color: green; border-radius: 8px;")
        self.status_label.setText("Normal")
        self.message_label.setText(message)

    def set_thresholds(self, warning=75, critical=85):
        """Updates warning and critical thresholds"""
        self.warning_threshold = warning
        self.critical_threshold = critical

    def enable_demo_mode(self, enabled=True):
        """Cycles through alarm states automatically for demonstration"""
        self.demo_mode = enabled
        if enabled:
            self.demo_timer.start(3000)  # Every 3 seconds
        else:
            self.demo_timer.stop()
            self.clear_alarm()  # Reset to normal when demo stops

    def cycle_demo_states(self):
        """Rotates through the alarm states for demo mode"""
        if self.alarm_state == "Normal":
            self.set_warning_alarm("DEMO MODE: Warning state")
        elif self.alarm_state == "Warning":
            self.set_critical_alarm("DEMO MODE: Critical state")
        else:
            self.clear_alarm("DEMO MODE: Normal state")


# Test application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Alarm System Test")
    window.setGeometry(100, 100, 400, 300)

    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)

    # Create and add alarm system
    alarm = AlarmSystem()
    layout.addWidget(alarm)

    # Add slider for testing different levels
    slider_layout = QHBoxLayout()
    slider_label = QLabel("Water Level:")
    water_slider = QSlider(Qt.Horizontal)
    water_slider.setRange(0, 100)
    water_slider.setValue(50)
    water_slider.setTickPosition(QSlider.TicksBelow)
    water_slider.setTickInterval(10)
    
    level_display = QLabel("50%")
    level_display.setMinimumWidth(40)
    
    # Update alarm when slider changes
    def update_level(value):
        level_display.setText(f"{value}%")
        alarm.check_water_level("test-sensor", value)
    
    water_slider.valueChanged.connect(update_level)
    
    slider_layout.addWidget(slider_label)
    slider_layout.addWidget(water_slider)
    slider_layout.addWidget(level_display)
    layout.addLayout(slider_layout)

    # Demo mode toggle
    demo_check = QCheckBox("Demo Mode")
    demo_check.stateChanged.connect(lambda state: alarm.enable_demo_mode(state == Qt.Checked))
    layout.addWidget(demo_check)

    window.setCentralWidget(central_widget)
    window.show()

    sys.exit(app.exec_())