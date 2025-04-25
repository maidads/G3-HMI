from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt
from sensor_detail import SensorDetail

class SensorCard(QFrame):
    def __init__(self, title, description, dashboard, image_path=None):
        super().__init__()
        self.dashboard = dashboard
        self.title = title
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFrameShape(QFrame.NoFrame)
        self.setMaximumWidth(400)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
            QFrame:hover {
                background-color: #F5F5F5;
            }
        """)
        self.init_ui(description, image_path)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

    def init_ui(self, description, image_path):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(0, 12, 0, 12)

        img_label = QLabel()
        img_label.setFixedSize(200, 200)
        img_label.setContentsMargins(0, 0, 0, 0)

        if image_path:
            pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            pixmap = QPixmap(200, 200)
            pixmap.fill(Qt.lightGray)
        img_label.setPixmap(pixmap)

        img_wrapper = QVBoxLayout()
        img_wrapper.setContentsMargins(12, 12, 12, 12)
        img_wrapper.setSpacing(0)
        img_wrapper.setAlignment(Qt.AlignVCenter)
        img_wrapper.addWidget(img_label)

        img_container = QFrame()
        img_container.setLayout(img_wrapper)
        img_container.setFixedWidth(200)

        main_layout.addWidget(img_container)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(12)
        text_layout.setContentsMargins(12, 12, 12, 12)

        title_label = QLabel(self.title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))

        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: gray;")

        button = QPushButton("Go to")
        button.setFixedWidth(80)
        button.setStyleSheet("""
            QPushButton {
                background-color: #B0E0E6;
                color: black;
                border: none;
                border-radius: 6px;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #A0CCD5;
            }
        """)

        button.clicked.connect(self.open_detail_view)

        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)
        text_layout.addWidget(button)
        text_layout.addStretch()

        main_layout.addLayout(text_layout)
        self.setLayout(main_layout)

    def open_detail_view(self):
        self.dashboard.hide()
        self.detail_window = SensorDetail(self.title, self.dashboard)
        self.detail_window.show()
