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

        layout = QVBoxLayout()

        header = QLabel("Sensors")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setStyleSheet("color: white;")
        subheader = QLabel("Tryck på Go to för att se detaljer")
        subheader.setStyleSheet("color: #d0f0f0;")
        layout.addWidget(header)
        layout.addWidget(subheader)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        sensor_layout = QVBoxLayout()

        sensor_layout.addWidget(SensorCard("Sensor 1", "Info om Sensor 1", self))
        sensor_layout.addWidget(SensorCard("Sensor 2", "Info om Sensor 2", self))
        sensor_layout.addWidget(SensorCard("Sensor 3", "Info om Sensor 3", self))

        container.setLayout(sensor_layout)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
