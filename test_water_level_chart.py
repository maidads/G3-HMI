# test_water_level_chart.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox
from PyQt5.QtCore import Qt
from water_level_chart import WaterLevelChart

class TestWindow(QMainWindow):
    """Test window for the water level chart component"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Water Level Chart Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Add label
        title = QLabel("Water Level History")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Add sensor selector
        sensor_layout = QVBoxLayout()
        sensor_label = QLabel("Select Sensor:")
        self.sensor_combo = QComboBox()
        self.sensor_combo.addItems(["Sensor 1", "Sensor 2", "Sensor 3"])
        self.sensor_combo.currentTextChanged.connect(self.update_chart)
        sensor_layout.addWidget(sensor_label)
        sensor_layout.addWidget(self.sensor_combo)
        layout.addLayout(sensor_layout)
        
        # Add chart
        self.chart = WaterLevelChart()
        layout.addWidget(self.chart)
        
        # Set central widget
        self.setCentralWidget(central_widget)
    
    def update_chart(self, sensor_name):
        """Update the chart when sensor selection changes"""
        if sensor_name:
            # Extract sensor ID from name (simple example)
            sensor_id = int(sensor_name.split()[-1])
            self.chart.update_chart(sensor_id)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())