import random
from PyQt6.QtCore import QObject, pyqtSignal


class BatteryModel(QObject):
    """Model representing battery data and state"""

    # Signals to notify observers of changes
    batteryChanged = pyqtSignal(dict)
    criticalLevelReached = pyqtSignal()

    def __init__(self, use_mock=True, initial_percent=70):
        super().__init__()
        self.use_mock = use_mock
        self.percent = initial_percent
        self.power_plugged = False
        self._critical_threshold = 20

    def update(self):
        """Update battery status"""
        if self.use_mock:
            # For mock battery, update to random values
            old_percent = self.percent
            self.percent = random.randint(0, 100)

            # Random power state change (20% chance)
            if random.random() < 0.2:
                self.power_plugged = not self.power_plugged

            # Check if battery has entered critical level
            if old_percent > self._critical_threshold and self.percent <= self._critical_threshold:
                self.criticalLevelReached.emit()
        else:
            # For real battery, try to get data from system
            self._get_real_battery_info()

        # Notify observers of the change
        self.batteryChanged.emit(self.get_state())

    def toggle_power(self):
        """Toggle power connection state"""
        self.power_plugged = not self.power_plugged
        self.batteryChanged.emit(self.get_state())

    def get_state(self):
        """Return current battery state as a dictionary"""
        return {
            "percent": self.percent,
            "plugged": self.power_plugged,
            "available": True
        }

    def _get_real_battery_info(self):
        """Get real battery information if possible"""
        try:
            import psutil
            battery = psutil.sensors_battery()
            if battery:
                old_percent = self.percent
                self.percent = battery.percent
                self.power_plugged = battery.power_plugged

                # Check if battery has entered critical level
                if old_percent > self._critical_threshold and self.percent <= self._critical_threshold:
                    self.criticalLevelReached.emit()
            else:
                # No battery found
                pass
        except (ImportError, AttributeError, NotImplementedError):
            # psutil not available or other error
            pass