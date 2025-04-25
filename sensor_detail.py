from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

class SensorDetail(QWidget):
    def __init__(self, sensor_name, dashboard_window):
        super().__init__()
        self.dashboard_window = dashboard_window
        self.setWindowTitle(f"{sensor_name} - Details")
        self.showFullScreen()

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#B0E0E6'))
        self.setPalette(palette)

        layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setFixedSize(80, 30)
        back_btn.setStyleSheet("background-color: white; color: black; font-weight: bold;")
        back_btn.clicked.connect(self.go_back)
        top_bar.addWidget(back_btn)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        self.setLayout(layout)


    def go_back(self):
        self.dashboard_window.setWindowState(Qt.WindowNoState)
        self.dashboard_window.show()
        self.dashboard_window.showFullScreen()
        self.close()
