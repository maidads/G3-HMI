# .\battery_monitor.py
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class BatteryMonitor(QWidget):
    """
    Displays battery level with color-coded progress bar:
    - Green (Good > 30%)
    - Orange (Low <= 30%)
    - Red (Critical <= 15%)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.battery_level = 100  # Default to full battery
        self.init_ui()

    def init_ui(self):
        """Sets up the battery monitor display"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Progress bar for visual representation
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(self.battery_level)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: green;
                border-radius: 4px;
                margin: 0px;
            }
        """)

        # Percentage display
        self.level_label = QLabel(f"{self.battery_level}%")
        self.level_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.level_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.level_label)
        self.update_bar_color()  # Set initial color

    def set_level(self, level):
        """Updates the battery level display"""
        self.battery_level = max(0, min(100, int(level)))
        self.level_label.setText(f"{self.battery_level}%")
        self.progress_bar.setValue(self.battery_level)
        self.update_bar_color()

    def update_bar_color(self):
        """Changes the progress bar color based on battery level"""
        if self.battery_level <= 15:
            color = "red"  # Critical
        elif self.battery_level <= 30:
            color = "orange"  # Low
        else:
            color = "green"  # Good

        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid grey;
                border-radius: 5px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 4px;
                margin: 0px;
            }}
        """)


# Test code
if __name__ == "__main__":
    app = QApplication(sys.argv)
    battery_widget = BatteryMonitor()
    battery_widget.set_level(75)
    battery_widget.setWindowTitle("Battery Monitor Test")
    battery_widget.setGeometry(100, 100, 200, 150)
    battery_widget.show()
    sys.exit(app.exec_())