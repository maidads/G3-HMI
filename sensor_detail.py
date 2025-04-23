from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
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

        main_layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setFixedSize(80, 30)
        back_btn.setStyleSheet("background-color: white; color: black; font-weight: bold;")
        back_btn.clicked.connect(self.close)
        top_bar.addWidget(back_btn)
        top_bar.addStretch()

        main_layout.addLayout(top_bar)

        label = QLabel("Detaljsidan...")
        label.setFont(QFont("Arial", 18, QFont.Bold))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)

        main_layout.addStretch()
        main_layout.addWidget(label)
        main_layout.addStretch()

        self.setLayout(main_layout)
