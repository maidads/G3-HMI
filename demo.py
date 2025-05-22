from PyQt6 import QtWidgets
from models.battery_model import BatteryModel
from views.battery_view import BatteryView
from controllers.battery_controller import BatteryController


def main():
    app = QtWidgets.QApplication([])

    # Create MVC components
    model = BatteryModel(use_mock=True)
    view = BatteryView()
    controller = BatteryController(model, view, update_interval=8000)

    # Start the controller
    controller.start()

    # Run the application
    app.exec()


if __name__ == "__main__":
    main()