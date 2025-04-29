from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class BatteryMonitor(QWidget):
    """
    Simple battery level monitor for sensors.
    Displays a battery percentage and visual indicator.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.battery_level = 100
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface components"""
        layout = QVBoxLayout(self)
        
        # Title label
        title_label = QLabel("Battery")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        
        # Battery level indicator
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(self.battery_level)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: green;
                border-radius: 5px;
            }
        """)
        
        # Battery level label
        self.level_label = QLabel(f"{self.battery_level}%")
        self.level_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.level_label.setAlignment(Qt.AlignCenter)
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.level_label)
        
        self.setLayout(layout)
    
    def set_level(self, level):
        """
        Set the battery level (0-100%)
        """
        # Ensure level is within valid range
        self.battery_level = max(0, min(100, level))
        
        # Update the UI
        self.level_label.setText(f"{self.battery_level}%")
        self.progress_bar.setValue(self.battery_level)
        
        # Update progress bar color based on level
        if self.battery_level <= 15:
            # Red for critical
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid grey;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: red;
                    border-radius: 5px;
                }
            """)
        elif self.battery_level <= 30:
            # Orange for low
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid grey;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: orange;
                    border-radius: 5px;
                }
            """)
        else:
            # Green for good
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid grey;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: green;
                    border-radius: 5px;
                }
            """)


# Simple test code when run directly
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    battery = BatteryMonitor()
    battery.set_level(75)
    battery.show()
    sys.exit(app.exec_())