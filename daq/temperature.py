"""
Temperature Data Acquisition Module
Collects system temperature data for system monitoring
"""

import psutil
import random

class TemperatureMonitor:
    """Simple temperature monitoring class for data acquisition."""
    
    def __init__(self):
        self.name = "Temperature"
        self.unit = "°C"
    
    def read_data(self):
        """
        Read current system temperature.
        Returns: float - Temperature in Celsius
        Note: Falls back to simulated data if hardware sensors unavailable
        """
        try:
            # Try to get real temperature data
            temps = psutil.sensors_temperatures()
            if temps:
                # Get first available temperature sensor
                for name, entries in temps.items():
                    if entries:
                        return round(entries[0].current, 1)
            
            # Fallback to simulated temperature (for demonstration)
            return self._simulate_temperature()
            
        except Exception as e:
            print(f"Error reading temperature data: {e}")
            print(f"Temperature acquisition is only available for LINUX systems")
            print(f" ")
            return self._simulate_temperature()
    
    def _simulate_temperature(self):
        """
        Simulate temperature data for systems without sensors.
        Returns: float - Simulated temperature
        """
        # Simple simulation: base temp + some variation
        base_temp = 45.0
        variation = random.uniform(-10, 20)
        return round(base_temp + variation, 1)
    
    def get_status(self):
        """
        Get temperature status based on current reading.
        Returns: str - Status description
        """
        temp = self.read_data()
        if temp < 60:
            return "Normal"
        elif temp < 80:
            return "Warm"
        else:
            return "Hot"