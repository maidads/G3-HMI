from PyQt6 import QtWidgets
from models.battery_model import BatteryModel
from views.battery_view import BatteryView
from controllers.battery_controller import BatteryController


class PowerBar(QtWidgets.QWidget):



    def __init__(self, steps=5, update_interval=8000, use_mock=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create MVC components
        self._model = BatteryModel(use_mock=use_mock)
        self._view = BatteryView()
        self._controller = BatteryController(self._model, self._view, update_interval=update_interval)

        # Set up layout to embed the view inside this widget
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._view)
        self.setLayout(layout)

        # Forward window title and size from view
        self.setWindowTitle(self._view.windowTitle())
        self.resize(self._view.size())

    def show(self):
        """Show the widget and start the controller"""
        super().show()
        self._controller.start()