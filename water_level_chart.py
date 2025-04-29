# water_level_chart.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from datetime import datetime, timedelta

class WaterLevelChart(QWidget):
    """
    Component to display water level history as a line chart.
    Shows water level readings over the past 7 days.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        """Initialize the UI components"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create matplotlib figure and canvas
        self.figure = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        
        # Add canvas to layout
        layout.addWidget(self.canvas)
        
        # Display placeholder data
        self.update_chart()
        
    def update_chart(self, sensor_id=None):
        """
        Update the chart with water level data.
        Currently uses placeholder data.
        
        Args:
            sensor_id: Optional sensor ID to filter data
        """
        # Clear previous plot
        self.figure.clear()
        
        # Create a new subplot
        ax = self.figure.add_subplot(111)
        
        # Generate dates for the last 7 days
        dates = [datetime.now() - timedelta(days=i) for i in range(7, 0, -1)]
        date_labels = [date.strftime('%m-%d') for date in dates]
        
        # Generate placeholder water level data (50-80%)
        # Use a simpler approach for seed - hash can produce values outside the allowed range
        np.random.seed(42 if not sensor_id else (sensor_id % 100))
        water_levels = np.random.uniform(50, 80, size=7)
        
        # Plot the data
        ax.plot(date_labels, water_levels, marker='o', linestyle='-', color='blue')
        
        # Add warning threshold line (example: 75%)
        ax.axhline(y=75, color='orange', linestyle='--', alpha=0.7, label='Warning')
        
        # Add critical threshold line (example: 85%)
        ax.axhline(y=85, color='red', linestyle='--', alpha=0.7, label='Critical')
        
        # Configure the chart
        ax.set_title('Water Level - Past 7 Days')
        ax.set_xlabel('Date')
        ax.set_ylabel('Water Level (%)')
        ax.set_ylim(0, 100)  # Water level percentage range
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Update the canvas
        self.canvas.draw()


# Simple test code when run directly
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("Water Level Chart Test")
    window.setGeometry(100, 100, 600, 400)
    
    chart = WaterLevelChart()
    window.setCentralWidget(chart)
    window.show()
    
    sys.exit(app.exec_())