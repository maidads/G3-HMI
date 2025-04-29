# .\test_battery_monitor.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSlider, QWidget, QLabel
from PyQt5.QtCore import Qt
# Import the component we want to test
from battery_monitor import BatteryMonitor

class TestWindow(QMainWindow):
    """A simple window for testing the BatteryMonitor widget interactively."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Battery Monitor Test")
        self.setGeometry(100, 100, 250, 200) # Adjusted size

        # Main container widget
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15) # Add spacing between elements

        instructions = QLabel("Adjust the slider to change the battery level.")
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)

        # Create and add the BatteryMonitor instance
        self.battery = BatteryMonitor()
        layout.addWidget(self.battery)

        # --- Slider control ---
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(100) # Start at full battery
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        # Connect the slider's value change to our update function
        self.slider.valueChanged.connect(self.update_battery_level)
        layout.addWidget(self.slider)

        self.setCentralWidget(central_widget)

    def update_battery_level(self, value):
        """Called when the slider value changes."""
        # Tell the battery monitor widget to update its display.
        self.battery.set_level(value)

# Standard way to run the test application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())