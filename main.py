from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QSlider, QApplication, QGraphicsDropShadowEffect
import random
import sys

from Widgets import CircularProgress
#import uis
from ui_main import Ui_MainWindow
from ui_splash_screen import Ui_SplashScreen

class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()  # Create an instance of the class
        self.ui.setupUi(self)
        #Remove title bar
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


        #import circular progress
        self.progress = CircularProgress()
        self.progress.width = 270
        self.progress.height = 270
        self.progress.value = 0
        self.progress.setFixedSize(self.progress.width, self.progress.height)
        self.progress.move(15, 15)
        self.progress.font_size = 40
        self.progress.add_shadow(True)
        self.progress.bg_color = QColor(68, 71, 90, 140)
        self.progress.setParent(self.ui.centralwidget)
        self.progress.show()

        # Add Drop Shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)

        #Q timer or randNr
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(80)

        #Variables for progress simulation

        self.counter = 0
        self.progress_speed = 1.0
        self.jump_size = 0

        self.show()
        #RandNum progress increments

    def update_progress(self):
        self.counter += 1

        #every 10 counts, randnum the progress speed and jump size-
        if self.counter % 10 == 0:
            self.progress_speed = random.uniform(0.5, 1.5)
            self.jump_size = random.randint(1, 3)

            #calculate new progress value with random elements
        new_value = self.progress.value + (self.jump_size * self.progress_speed)

        #Handler for the different phases - slow down near completion
        if new_value >= 100:
            new_value = 100
            self.timer.stop()
            # Transition to main app after a short delay
            QTimer.singleShot(500, self.close_splash)
        elif new_value >= 80:
            # Slow down near completion
            new_value = min(new_value, self.progress.value + 0.5)

        self.progress.set_value(int(new_value))
        # Update loading text based on progress
        if new_value < 25:
            self.ui.loading.setText("Loading modules...")
        elif new_value < 50:
            self.ui.loading.setText("Initializing...")
        elif new_value < 75:
            self.ui.loading.setText("Loading UI components...")
        else:
            self.ui.loading.setText("Almost done...")

    def close_splash(self):
        # for launching your main application window
        # For example:
        # self.main = MainWindow()
        # self.main.show()
        self.close()



class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()  # Create an instance of the class
        self.ui.setupUi(self)
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec())