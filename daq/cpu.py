"""
CPU Data Acquisition Module
Collects CPU usage data for system monitoring
"""

import psutil

class CPUMonitor:
    """Simple CPU monitoring class for data acquisition."""
    
    def __init__(self):
        self.name = "CPU"
        self.unit = "%"
    
    def read_data(self):
        """
        Read current CPU usage percentage.
        Returns: float - CPU usage percentage (0-100)
        """
        try:
            usage = psutil.cpu_percent(interval=0.1)
            return round(usage, 1)
        except Exception as e:
            print(f"Error reading CPU data: {e}")
            return 0.0
    
    def get_status(self):
        """
        Get CPU status based on current usage.
        Returns: str - Status description
        """
        usage = self.read_data()
        if usage < 50:
            return "Normal"
        elif usage < 80:
            return "High"
        else:
            return "Critical"