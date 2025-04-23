from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from sensor_detail import SensorDetail

class SensorCard(QFrame):
    def __init__(self, title, description, dashboard, image_path=None):
        super().__init__()
        self.dashboard = dashboard
        self.title = title
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet("background-color: white; border-radius: 8px;")
        self.init_ui(description, image_path)

    def init_ui(self, description, image_path):
        layout = QHBoxLayout()

        img_label = QLabel()
        if image_path:
            pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio)
        else:
            pixmap = QPixmap(100, 100)
            pixmap.fill(Qt.lightGray)
        img_label.setPixmap(pixmap)
        layout.addWidget(img_label)

        text_layout = QVBoxLayout()
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: gray;")

        button = QPushButton("Go to")
        button.setFixedWidth(80)
        button.clicked.connect(self.open_detail_view)

        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)
        text_layout.addWidget(button)
        layout.addLayout(text_layout)

        self.setLayout(layout)

    def open_detail_view(self):
        self.dashboard.hide()
        self.detail_window = SensorDetail(self.title, self.dashboard)
        self.detail_window.show()
