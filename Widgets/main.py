import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QSlider, QApplication


# Import Circular Project from Widgets package
from Widgets.circular_progress import CircularProgress
# Alternatively, you can use:
# from Widgets import CircularProgress


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # Resize Window
        self.resize(500, 500)

        #Remove Title-bar
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        #Create Container and layout
        self.container = QFrame()
        self.container.setStyleSheet("background-color: transparent;")
        self.layout = QVBoxLayout()

        # Create Circular Progress
        self.circular_progress = CircularProgress()
        self.circular_progress.value = 50
        self.circular_progress.suffix = " %"
        self.circular_progress.font_size = 24
        self.circular_progress.progress_width = 10
        self.circular_progress.text_color = QColor("#FFFFFF")
        self.circular_progress.progress_color = QColor("#FFFFFF")
        self.circular_progress.progress_rounded_cap = True
        self.circular_progress.add_shadow(True)
        self.circular_progress.setMinimumSize(self.circular_progress.width, self.circular_progress.height)


        #add slider
        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.valueChanged.connect(self.change_value)  # type: ignore
        self.slider.setRange(0, 100)


        # Add Widgets - FIXED PARAMETERS
        self.layout.addWidget(self.circular_progress, 0, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.slider, 0, Qt.AlignmentFlag.AlignCenter)


        #set central widget
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        #show window
        self.show()

        #Change value
    def change_value(self, value):
        self.circular_progress.set_value(value)  # Changed from self.progress to self.circular_progress


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())