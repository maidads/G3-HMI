# mock_database.py
import json
import os
import random
from datetime import datetime, timedelta
import numpy as np

class MockDatabase:
    """
    Simulates a database for sensor data with generated placeholder values.
    Stores and retrieves water level, battery level, and historical data.
    """
    
    FILENAME = "sensor_data.json"
    
    def __init__(self):
        self.data = self._load_data() or self._create_initial_data()
        
    def _load_data(self):
        """Load existing data from file if available"""
        if os.path.exists(self.FILENAME):
            try:
                with open(self.FILENAME, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading data: {e}")
        return None
    
    def _save_data(self):
        """Save current data to file"""
        try:
            with open(self.FILENAME, 'w') as f:
                json.dump(self.data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def _create_initial_data(self):
        """Generate initial data structure with sensor info"""
        sensors = {
            "Sensor 1": {"name": "Main Tank", "enabled": True, "max_level": 100, "offset": 0},
            "Sensor 2": {"name": "Reserve Tank", "enabled": True, "max_level": 100, "offset": 0},
            "Sensor 3": {"name": "Overflow Tank", "enabled": True, "max_level": 100, "offset": 0}
        }
        
        # Generate 7 days of historical data for each sensor
        now = datetime.now()
        for sensor_id, sensor in sensors.items():
            # Create readings array for historical data
            sensor["readings"] = []
            
            # Generate different patterns for each sensor
            seed = int(sensor_id.split()[-1])
            np.random.seed(seed)
            
            for i in range(7):
                date = (now - timedelta(days=6-i)).strftime("%Y-%m-%d")
                # More variation for interesting charts
                base_level = 50 + seed * 5
                level = base_level + np.random.normal(0, 5) + i * 2
                level = max(10, min(95, level))  # Keep within reasonable range
                
                # Add a reading for this day
                sensor["readings"].append({
                    "date": date,
                    "water_level": round(level, 1),
                    "battery_level": round(90 - i * (3 - seed), 1)
                })
            
            # Current readings
            sensor["current_water_level"] = sensor["readings"][-1]["water_level"]
            sensor["current_battery_level"] = sensor["readings"][-1]["battery_level"]
            sensor["last_updated"] = now.strftime("%Y-%m-%d %H:%M:%S")
        
        data = {
            "sensors": sensors,
            "settings": {
                "warning_threshold": 75,
                "critical_threshold": 85,
                "update_interval": 15  # minutes
            }
        }
        
        return data
    
    def get_sensors(self):
        """Return list of all sensor IDs"""
        return list(self.data["sensors"].keys())
    
    def get_sensor_data(self, sensor_id):
        """Get full data for a specific sensor"""
        if sensor_id in self.data["sensors"]:
            return self.data["sensors"][sensor_id]
        return None
    
    def get_current_level(self, sensor_id):
        """Get current water level for a sensor"""
        if sensor_id in self.data["sensors"]:
            return self.data["sensors"][sensor_id]["current_water_level"]
        return None
    
    def get_battery_level(self, sensor_id):
        """Get current battery level for a sensor"""
        if sensor_id in self.data["sensors"]:
            return self.data["sensors"][sensor_id]["current_battery_level"]
        return None
    
    def get_historical_data(self, sensor_id, days=7):
        """Get historical readings for a sensor"""
        if sensor_id in self.data["sensors"]:
            readings = self.data["sensors"][sensor_id]["readings"]
            return readings[-days:] if days < len(readings) else readings
        return []
    
    def update_sensor_reading(self, sensor_id, water_level=None, battery_level=None):
        """Update current readings for a sensor"""
        if sensor_id in self.data["sensors"]:
            sensor = self.data["sensors"][sensor_id]
            
            if water_level is not None:
                sensor["current_water_level"] = water_level
            
            if battery_level is not None:
                sensor["current_battery_level"] = battery_level
            
            now = datetime.now()
            sensor["last_updated"] = now.strftime("%Y-%m-%d %H:%M:%S")
            
            # Add to readings if it's a new day
            today = now.strftime("%Y-%m-%d")
            if not sensor["readings"] or sensor["readings"][-1]["date"] != today:
                sensor["readings"].append({
                    "date": today,
                    "water_level": sensor["current_water_level"],
                    "battery_level": sensor["current_battery_level"]
                })
                # Keep only last 30 days
                if len(sensor["readings"]) > 30:
                    sensor["readings"].pop(0)
            
            self._save_data()
            return True
        return False
    
    def get_settings(self):
        """Get application settings"""
        return self.data["settings"]
    
    def save_settings(self, settings):
        """Save application settings"""
        # Update only the keys that exist in the settings parameter
        for key, value in settings.items():
            self.data["settings"][key] = value
        
        success = self._save_data()
        return success
    
    def update_sensor_settings(self, sensor_id, settings_dict):
        """Update settings for a specific sensor"""
        if sensor_id in self.data["sensors"]:
            # Update sensor settings without changing readings
            for key, value in settings_dict.items():
                if key not in ["readings", "current_water_level", "current_battery_level", "last_updated"]:
                    self.data["sensors"][sensor_id][key] = value
            
            self._save_data()
            return True
        return False
    
    def export_to_csv(self, filename=None):
        """Export all sensor data to a CSV file"""
        if not filename:
            filename = f"water_level_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, 'w') as f:
                # Write header
                f.write("Sensor,Date,Water Level (%),Battery Level (%)\n")
                
                # Write data for each sensor
                for sensor_id in self.get_sensors():
                    sensor_data = self.get_sensor_data(sensor_id)
                    sensor_name = sensor_data.get("name", sensor_id)
                    
                    for reading in sensor_data["readings"]:
                        f.write(f"{sensor_name},{reading['date']},{reading['water_level']},{reading['battery_level']}\n")
            
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def simulate_update(self):
        """Simulate data update for all sensors"""
        for sensor_id in self.get_sensors():
            sensor = self.get_sensor_data(sensor_id)
            if sensor["enabled"]:
                # Small random change to water level
                water_change = random.uniform(-2, 2)
                new_water = max(10, min(95, sensor["current_water_level"] + water_change))
                
                # Small decrease in battery
                new_battery = max(0, sensor["current_battery_level"] - random.uniform(0, 0.1))
                
                self.update_sensor_reading(sensor_id, new_water, new_battery)
        return True