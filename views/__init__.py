# views/__init__.py

# Import the main view classes to make them available at the package level
from .battery_view import BatteryView, BatteryBarWidget

# Define what gets imported when someone uses 'from views import *'
__all__ = ['BatteryView', 'BatteryBarWidget']
