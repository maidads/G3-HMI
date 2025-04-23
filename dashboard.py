import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtGui import QPalette, QColor, QFont
from sensor_card import SensorCard

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.showFullScreen()
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#22C9C1'))
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        header = QLabel("Sensors")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setStyleSheet("color: white;")
        subheader = QLabel("Subheading")
        subheader.setStyleSheet("color: #d0f0f0;")
        main_layout.addWidget(header)
        main_layout.addWidget(subheader)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        sensor_layout = QVBoxLayout()

        sensor_layout.addWidget(SensorCard("Sensor 1", "Detailed overview for Sensor 1"))
        sensor_layout.addWidget(SensorCard("Sensor 2", "Detailed overview for Sensor 2"))
        sensor_layout.addWidget(SensorCard("Sensor 3", "Detailed overview for Sensor 3"))

        container.setLayout(sensor_layout)
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
