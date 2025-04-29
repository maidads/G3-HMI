# .\test_water_level_chart.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QComboBox)
from PyQt5.QtCore import Qt
# Import the component we want to test
from water_level_chart import WaterLevelChart

class TestWindow(QMainWindow):
    """A window for testing the WaterLevelChart widget."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Water Level Chart Test")
        self.setGeometry(100, 100, 700, 550) # Adjusted size

        # Main container widget
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)

        title = QLabel("Water Level History Chart")
        title.setFont(title.font()) # Get current font
        title.font().setPointSize(14) # Increase font size
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # --- Sensor Selector ---
        selector_layout = QHBoxLayout()
        selector_label = QLabel("Select Sensor (for placeholder data):")
        self.sensor_combo = QComboBox()
        # Add some dummy sensor names
        self.sensor_combo.addItems(["Sensor 1", "Sensor 2", "Sensor 3", "No Sensor ID"])
        # Update the chart when the selection changes
        self.sensor_combo.currentTextChanged.connect(self.update_chart_for_sensor)
        selector_layout.addWidget(selector_label)
        selector_layout.addWidget(self.sensor_combo)
        selector_layout.addStretch()
        layout.addLayout(selector_layout)

        # --- Chart Widget ---
        self.chart_widget = WaterLevelChart()
        # Allow the chart to take up most of the space
        layout.addWidget(self.chart_widget, stretch=1)

        self.setCentralWidget(central_widget)

        # Initial chart update based on default selection
        self.update_chart_for_sensor(self.sensor_combo.currentText())

    def update_chart_for_sensor(self, sensor_name):
        """Called when the QComboBox selection changes."""
        sensor_id = None # Default to no specific ID
        if sensor_name:
            # Try to extract a number from the end of the sensor name.
            # This is just for varying the placeholder data.
            parts = sensor_name.split()
            if parts and parts[-1].isdigit():
                try:
                    sensor_id = int(parts[-1])
                except ValueError:
                    pass # Ignore if it's not a valid number

        print(f"Updating chart for sensor: '{sensor_name}' (using ID: {sensor_id})")
        # Tell the chart widget to redraw, potentially with a new seed for data.
        self.chart_widget.update_chart(sensor_id)

# Standard way to run the test application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())