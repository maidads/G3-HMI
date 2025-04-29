# .\test_alarm_system.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QSlider, QCheckBox)
from PyQt5.QtCore import Qt
# Import the component we want to test
from alarm_system import AlarmSystem

class TestWindow(QMainWindow):
    """A simple window specifically for testing the AlarmSystem widget."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Alarm System Test")
        self.setGeometry(100, 100, 450, 350) # Adjusted size slightly

        # Main container widget
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        instructions = QLabel("Use the slider to simulate water levels and test alarm thresholds.")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setWordWrap(True) # Allow text to wrap
        layout.addWidget(instructions)

        # Create and add the AlarmSystem instance
        self.alarm = AlarmSystem()
        # You could set custom thresholds for testing here if needed:
        # self.alarm.set_thresholds(warning=60, critical=80)
        layout.addWidget(self.alarm)

        # --- Slider controls ---
        slider_layout = QHBoxLayout()
        slider_label = QLabel("Water Level:")
        self.water_slider = QSlider(Qt.Horizontal)
        self.water_slider.setRange(0, 100)
        self.water_slider.setValue(50) # Start at a normal level
        self.water_slider.setTickPosition(QSlider.TicksBelow)
        self.water_slider.setTickInterval(10)

        self.level_display = QLabel(f"{self.water_slider.value()}%")
        self.level_display.setMinimumWidth(40) # Ensure space for "100%"

        # Connect the slider's value change to our update function
        self.water_slider.valueChanged.connect(self.update_level)

        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(self.water_slider)
        slider_layout.addWidget(self.level_display)
        layout.addLayout(slider_layout)

        # --- Demo Mode Checkbox ---
        demo_check = QCheckBox("Enable Demo Mode (Cycles states)")
        # Connect checkbox state changes to the alarm system's demo mode toggle
        demo_check.stateChanged.connect(
            lambda state: self.alarm.enable_demo_mode(state == Qt.Checked)
        )
        layout.addWidget(demo_check)

        layout.addStretch() # Add some space at the bottom

        self.setCentralWidget(central_widget)

        # --- Connect to Signals for Feedback ---
        # Print messages when alarms trigger or clear.
        self.alarm.alarm_triggered.connect(self.handle_alarm_triggered)
        self.alarm.alarm_cleared.connect(self.handle_alarm_cleared)

    def update_level(self, value):
        """Called when the slider value changes."""
        self.level_display.setText(f"{value}%")
        # Pass the new level to the alarm system for checking.
        self.alarm.check_water_level("test-sensor-01", value)

    def handle_alarm_triggered(self, sensor_id, message):
        """Called when the alarm_triggered signal is emitted."""
        print(f"SIGNAL RECEIVED: Alarm Triggered! Sensor: {sensor_id}, Message: {message}")
        # In a real app, you might log this, send an alert, etc.

    def handle_alarm_cleared(self, sensor_id):
        """Called when the alarm_cleared signal is emitted."""
        print(f"SIGNAL RECEIVED: Alarm Cleared. Sensor: {sensor_id}")

# Standard way to run the test application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())