"""
Disk Data Acquisition Module
Collects disk usage data for system monitoring
"""

import psutil
import os

class DiskMonitor:
    """Simple disk monitoring class for data acquisition."""
    
    def __init__(self, path="/"):
        self.name = "Disk"
        self.unit = "%"
        self.path = path
    
    def read_data(self):
        """
        Read current disk usage percentage.
        Returns: float - Disk usage percentage (0-100)
        """
        try:
            usage = psutil.disk_usage(self.path)
            percent = (usage.used / usage.total) * 100
            return round(percent, 1)
        except Exception as e:
            print(f"Error reading disk data: {e}")
            return 0.0
    
    def get_free_gb(self):
        """
        Get free disk space in GB.
        Returns: float - Free space in GB
        """
        try:
            usage = psutil.disk_usage(self.path)
            return round(usage.free / (1024**3), 2)
        except Exception:
            return 0.0
    
    def get_status(self):
        """
        Get disk status based on current usage.
        Returns: str - Status description
        """
        usage = self.read_data()
        if usage < 80:
            return "Normal"
        elif usage < 95:
            return "High"
        else:
            return "Critical"