# alarm_system.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

class AlarmSystem(QWidget):
    """
    Alarm component for monitoring water levels.
    Displays status and warnings when thresholds are exceeded.
    
    Emits signals when alarm states change that can be connected
    to external notification systems.
    """
    
    # Define signals
    alarm_triggered = pyqtSignal(str, str)  # (sensor_id, message)
    alarm_cleared = pyqtSignal(str)  # sensor_id
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Default thresholds (can be configured)
        self.warning_threshold = 75
        self.critical_threshold = 85
        
        # Alarm state
        self.alarm_state = "Normal"  # "Normal", "Warning", or "Critical"
        
        # Initialize UI
        self.init_ui()
        
        # Demo mode - automatically cycle states
        self.demo_mode = False
        self.demo_timer = QTimer(self)
        self.demo_timer.timeout.connect(self.cycle_demo_states)
        
    def init_ui(self):
        """Initialize the user interface"""
        # Main layout
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Alarm Status")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Status display
        self.status_frame = QFrame()
        self.status_frame.setFrameShape(QFrame.Box)
        self.status_frame.setLineWidth(2)
        self.status_frame.setStyleSheet("background-color: green; border-radius: 8px;")
        self.status_frame.setMinimumHeight(40)
        
        # Status text
        status_layout = QVBoxLayout(self.status_frame)
        self.status_label = QLabel("Normal")
        self.status_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: white;")
        status_layout.addWidget(self.status_label)
        
        # Message text
        self.message_label = QLabel("Water level within safe limits")
        self.message_label.setAlignment(Qt.AlignCenter)
        
        # Add widgets to layout
        layout.addWidget(self.status_frame)
        layout.addWidget(self.message_label)
        
        self.setLayout(layout)
    
    def check_water_level(self, sensor_id, water_level):
        """
        Check if water level exceeds thresholds and update alarm state.
        
        Args:
            sensor_id: ID of the sensor being checked
            water_level: Current water level (percentage)
        """
        old_state = self.alarm_state
        
        # Check against thresholds
        if water_level >= self.critical_threshold:
            self.set_critical_alarm(f"CRITICAL: Water level at {water_level}%")
            if old_state != "Critical":
                self.alarm_triggered.emit(sensor_id, f"Critical water level: {water_level}%")
        elif water_level >= self.warning_threshold:
            self.set_warning_alarm(f"WARNING: Water level at {water_level}%")
            if old_state != "Warning":
                self.alarm_triggered.emit(sensor_id, f"Warning water level: {water_level}%")
        else:
            self.clear_alarm("Water level within safe limits")
            if old_state != "Normal":
                self.alarm_cleared.emit(sensor_id)
    
    def set_warning_alarm(self, message):
        """Set alarm state to Warning"""
        self.alarm_state = "Warning"
        self.status_frame.setStyleSheet("background-color: orange; border-radius: 8px;")
        self.status_label.setText("Warning")
        self.message_label.setText(message)
    
    def set_critical_alarm(self, message):
        """Set alarm state to Critical"""
        self.alarm_state = "Critical"
        self.status_frame.setStyleSheet("background-color: red; border-radius: 8px;")
        self.status_label.setText("Critical")
        self.message_label.setText(message)
    
    def clear_alarm(self, message="Normal operation"):
        """Clear alarm state"""
        self.alarm_state = "Normal"
        self.status_frame.setStyleSheet("background-color: green; border-radius: 8px;")
        self.status_label.setText("Normal")
        self.message_label.setText(message)
    
    def set_thresholds(self, warning=75, critical=85):
        """
        Set warning and critical thresholds
        
        Args:
            warning: Warning threshold percentage
            critical: Critical threshold percentage
        """
        self.warning_threshold = warning
        self.critical_threshold = critical
    
    def enable_demo_mode(self, enabled=True):
        """
        Enable/disable demo mode to cycle through alarm states
        Used for testing and demonstration
        """
        self.demo_mode = enabled
        if enabled:
            self.demo_timer.start(3000)  # Cycle every 3 seconds
        else:
            self.demo_timer.stop()
    
    def cycle_demo_states(self):
        """Cycle through alarm states for demonstration"""
        if self.alarm_state == "Normal":
            self.set_warning_alarm("DEMO MODE: Warning state")
        elif self.alarm_state == "Warning":
            self.set_critical_alarm("DEMO MODE: Critical state")
        else:
            self.clear_alarm("DEMO MODE: Normal state")


# Test code when run directly
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QHBoxLayout
    
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("Alarm System Test")
    window.setGeometry(100, 100, 400, 300)
    
    # Create central widget with layout
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    
    # Add alarm system
    alarm = AlarmSystem()
    layout.addWidget(alarm)
    
    # Add slider to test different water levels
    slider_layout = QHBoxLayout()
    slider_label = QLabel("Water Level:")
    water_slider = QSlider(Qt.Horizontal)
    water_slider.setMinimum(0)
    water_slider.setMaximum(100)
    water_slider.setValue(50)
    water_slider.setTickPosition(QSlider.TicksBelow)
    water_slider.setTickInterval(10)
    
    level_display = QLabel("50%")
    level_display.setMinimumWidth(40)
    
    # Connect slider to alarm check
    def update_level(value):
        level_display.setText(f"{value}%")
        alarm.check_water_level("test-sensor", value)
    
    water_slider.valueChanged.connect(update_level)
    
    slider_layout.addWidget(slider_label)
    slider_layout.addWidget(water_slider)
    slider_layout.addWidget(level_display)
    
    layout.addLayout(slider_layout)
    
    # Add demo mode checkbox
    demo_check = QCheckBox("Demo Mode")
    demo_check.stateChanged.connect(lambda state: alarm.enable_demo_mode(state == Qt.Checked))
    layout.addWidget(demo_check)
    
    window.setCentralWidget(central_widget)
    window.show()
    
    sys.exit(app.exec_())