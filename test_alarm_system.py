# test_alarm_system.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSlider, QCheckBox
from PyQt5.QtCore import Qt
from alarm_system import AlarmSystem

class TestWindow(QMainWindow):
    """Test window for the alarm system component"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Alarm System Test")
        self.setGeometry(100, 100, 500, 300)
        
        # Create central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Add instructions
        instructions = QLabel("Use the slider to test water level alarm thresholds")
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)
        
        # Add alarm system
        self.alarm = AlarmSystem()
        layout.addWidget(self.alarm)
        
        # Add slider to test different water levels
        slider_layout = QHBoxLayout()
        slider_label = QLabel("Water Level:")
        self.water_slider = QSlider(Qt.Horizontal)
        self.water_slider.setMinimum(0)
        self.water_slider.setMaximum(100)
        self.water_slider.setValue(50)
        self.water_slider.setTickPosition(QSlider.TicksBelow)
        self.water_slider.setTickInterval(10)
        
        self.level_display = QLabel("50%")
        self.level_display.setMinimumWidth(40)
        
        # Connect slider to alarm check
        self.water_slider.valueChanged.connect(self.update_level)
        
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(self.water_slider)
        slider_layout.addWidget(self.level_display)
        
        layout.addLayout(slider_layout)
        
        # Add demo mode checkbox
        demo_check = QCheckBox("Demo Mode (Cycle through states)")
        demo_check.stateChanged.connect(lambda state: self.alarm.enable_demo_mode(state == Qt.Checked))
        layout.addWidget(demo_check)
        
        # Set central widget
        self.setCentralWidget(central_widget)
        
        # Connect to alarm signals
        self.alarm.alarm_triggered.connect(self.handle_alarm)
        self.alarm.alarm_cleared.connect(self.handle_clear)
    
    def update_level(self, value):
        """Update when slider value changes"""
        self.level_display.setText(f"{value}%")
        self.alarm.check_water_level("test-sensor", value)
    
    def handle_alarm(self, sensor_id, message):
        """Handle alarm triggered signal"""
        print(f"ALARM: {sensor_id} - {message}")
        # In a real application, this could send notifications, etc.
    
    def handle_clear(self, sensor_id):
        """Handle alarm cleared signal"""
        print(f"CLEARED: {sensor_id} - Alarm condition no longer exists")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())