# .\sensor_card.py
from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout,
                             QPushButton, QSizePolicy, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt
from sensor_detail import SensorDetail

class SensorCard(QFrame):
    """
    Displays a sensor on the dashboard with basic info and navigation button.
    """
    def __init__(self, title, description, dashboard, image_path=None):
        super().__init__()
        self.dashboard = dashboard
        self.title = title

        # Set up card appearance
        self.setFrameShape(QFrame.NoFrame)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedWidth(600)
        self.setStyleSheet("""
            SensorCard {
                background-color: white;
                border-radius: 12px;
                margin-bottom: 10px;
            }
        """)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

        self.init_ui(description, image_path)

    def init_ui(self, description, image_path):
        """Creates the card content"""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Image section
        img_label = QLabel()
        img_size = 150
        img_label.setFixedSize(img_size, img_size)
        img_label.setAlignment(Qt.AlignCenter)

        # Use provided image or placeholder
        if image_path:
            pixmap = QPixmap(image_path)
        else:
            pixmap = QPixmap(img_size, img_size)
            pixmap.fill(Qt.lightGray)

        img_label.setPixmap(pixmap.scaled(img_size, img_size, 
                                         Qt.KeepAspectRatio, Qt.SmoothTransformation))
        main_layout.addWidget(img_label)

        # Text and button section
        text_layout = QVBoxLayout()
        text_layout.setSpacing(8)
        text_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel(self.title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setWordWrap(True)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #555;")
        desc_label.setWordWrap(True)

        # Detail button
        detail_button = QPushButton("Go to Details")
        detail_button.setFixedWidth(100)
        detail_button.setStyleSheet("""
            QPushButton {
                background-color: #5DADE2;
                color: white;
                border: none; border-radius: 6px;
                padding: 5px 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #3498DB; }
        """)
        detail_button.clicked.connect(self.open_detail_view)

        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)
        text_layout.addStretch()
        text_layout.addWidget(detail_button, alignment=Qt.AlignLeft)

        main_layout.addLayout(text_layout)
        main_layout.addStretch()

    def open_detail_view(self):
        """Opens the detail view for this sensor"""
        self.dashboard.hide()
        self.detail_window = SensorDetail(self.title, self.dashboard)
        self.detail_window.show()