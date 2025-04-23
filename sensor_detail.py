from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

class SensorDetail(QWidget):
    def __init__(self, sensor_name):
        super().__init__()
        self.setWindowTitle(f"{sensor_name} - Details")
        self.showFullScreen()

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#22C9C1'))
        self.setPalette(palette)

        layout = QVBoxLayout()

        label = QLabel("Detaljsidan...")
        label.setFont(QFont("Arial", 18, QFont.Bold))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)
        self.setLayout(layout)
