from PyQt6.QtCore import QObject, QTimer


class BatteryController(QObject):
    """Controller connecting battery model with views"""

    def __init__(self, model, view, update_interval=8000):
        super().__init__()
        self.model = model
        self.view = view

        # Connect model signals to view methods
        self.model.batteryChanged.connect(self.view.update_display)
        self.model.criticalLevelReached.connect(self.view.show_critical_warning)

        # Connect view signals to model methods
        self.view.powerToggleRequested.connect(self.model.toggle_power)

        # Set up timer for regular updates
        self._timer = QTimer()
        self._timer.setInterval(update_interval)  # 8 seconds
        self._timer.timeout.connect(self.model.update)

    def start(self):
        """Start the controller, show the view and begin updates"""
        # Initial update
        self.model.update()

        # Start the timer
        self._timer.start()

        # Show the view
        self.view.show()