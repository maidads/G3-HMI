# models/__init__.py

# Import main model classes to make them available at the package level
from .battery_model import BatteryModel

# Define what gets imported when someone uses 'from models import *'
__all__ = ['BatteryModel']