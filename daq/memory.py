"""
Memory Data Acquisition Module
Collects memory usage data for system monitoring
"""

import psutil

class MemoryMonitor:
    """Simple memory monitoring class for data acquisition."""
    
    def __init__(self):
        self.name = "Memory"
        self.unit = "%"
    
    def read_data(self):
        """
        Read current memory usage percentage.
        Returns: float - Memory usage percentage (0-100)
        """
        try:
            memory = psutil.virtual_memory()
            return round(memory.percent, 1)
        except Exception as e:
            print(f"Error reading memory data: {e}")
            return 0.0
    
    def get_available_gb(self):
        """
        Get available memory in GB.
        Returns: float - Available memory in GB
        """
        try:
            memory = psutil.virtual_memory()
            return round(memory.available / (1024**3), 2)
        except Exception:
            return 0.0
    
    def get_status(self):
        """
        Get memory status based on current usage.
        Returns: str - Status description
        """
        usage = self.read_data()
        if usage < 70:
            return "Normal"
        elif usage < 90:
            return "High"
        else:
            return "Critical"