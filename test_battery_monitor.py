import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSlider, QWidget, QLabel
from PyQt5.QtCore import Qt
from battery_monitor import BatteryMonitor

class TestWindow(QMainWindow):
    """Simple test window for the battery monitor component"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Battery Monitor Test")
        self.setGeometry(100, 100, 250, 300)
        
        # Create central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Add instructions
        instructions = QLabel("Adjust the slider to test battery levels")
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)
        
        # Add battery monitor
        self.battery = BatteryMonitor()
        layout.addWidget(self.battery)
        
        # Add slider for testing
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(100)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.update_battery)
        layout.addWidget(self.slider)
        
        # Set the central widget
        self.setCentralWidget(central_widget)
    
    def update_battery(self, value):
        """Update battery level based on slider value"""
        self.battery.set_level(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())