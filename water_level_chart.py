# .\water_level_chart.py
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QMainWindow
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from datetime import datetime, timedelta

class WaterLevelChart(QWidget):
    """
    Displays a chart showing water level history over the past 7 days.
    Currently uses placeholder data with variations based on sensor ID.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Default thresholds matching alarm system
        self.warning_threshold = 75
        self.critical_threshold = 85
        self.init_ui()

    def init_ui(self):
        """Sets up the chart widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create matplotlib figure and canvas
        self.figure = plt.figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)
        
        # Draw initial chart
        self.update_chart()

    def update_chart(self, sensor_id=None):
        """
        Updates the chart with data for the specified sensor.
        
        Args:
            sensor_id: Optional ID to generate consistent data for a specific sensor
        """
        # Clear previous plot
        self.figure.clear()

        # Create subplot
        ax = self.figure.add_subplot(111)

        # Generate dates for x-axis (last 7 days)
        today = datetime.now()
        dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
        date_labels = [date.strftime('%m-%d') for date in dates]

        # Generate placeholder water level data
        seed = 42 if sensor_id is None else (sensor_id % 1000) + 42
        np.random.seed(seed)
        water_levels = np.random.uniform(50, 80, size=7)

        # Plot the data
        ax.plot(date_labels, water_levels, marker='o', linestyle='-', 
               color='dodgerblue', linewidth=2, label='Water Level')

        # Add threshold lines
        ax.axhline(y=self.warning_threshold, color='orange', linestyle='--',
                  linewidth=1.5, alpha=0.8, label=f'Warning ({self.warning_threshold}%)')
        ax.axhline(y=self.critical_threshold, color='red', linestyle='--',
                  linewidth=1.5, alpha=0.8, label=f'Critical ({self.critical_threshold}%)')

        # Configure chart
        title = 'Water Level - Past 7 Days'
        if sensor_id:
            title += f" (Sensor {sensor_id})"
        ax.set_title(title, fontsize=12)
        ax.set_xlabel('Date', fontsize=10)
        ax.set_ylabel('Water Level (%)', fontsize=10)
        ax.set_ylim(0, 105)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(fontsize=9)

        # Improve date label readability
        self.figure.autofmt_xdate()
        
        # Ensure proper layout
        self.figure.tight_layout()
        
        # Update the canvas
        self.canvas.draw()


# Test code
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Water Level Chart Test")
    window.setGeometry(100, 100, 650, 450)

    chart = WaterLevelChart()
    window.setCentralWidget(chart)
    window.show()

    sys.exit(app.exec_())