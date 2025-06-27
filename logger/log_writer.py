"""
Log Writer Module
Handles data logging for system monitoring (DCS data historian functionality)
"""

import datetime
import csv
import os

class SystemLogger:
    """Simple data logger for system monitoring data."""
    
    def __init__(self, log_file="system_monitor.log"):
        self.log_file = log_file
        self.csv_file = "system_data.csv"
        self._initialize_csv()
    
    def _initialize_csv(self):
        """Initialize CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'CPU %', 'Memory %', 'Disk %', 'Temperature °C', 'Health'])
    
    def log_event(self, message, level="INFO"):
        """
        Log an event message with timestamp.
        
        Args:
            message (str): Event message to log
            level (str): Log level (INFO, WARNING, ERROR, CRITICAL)
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def log_system_data(self, cpu_usage, memory_usage, disk_usage, temperature, health_status):
        """
        Log system data to CSV file for historical analysis.
        
        Args:
            cpu_usage (float): CPU usage percentage
            memory_usage (float): Memory usage percentage
            disk_usage (float): Disk usage percentage
            temperature (float): System temperature
            health_status (str): Overall system health status
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(self.csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, cpu_usage, memory_usage, disk_usage, temperature, health_status])
        except Exception as e:
            print(f"Error writing system data to CSV: {e}")
    
    def log_alert(self, alert):
        """
        Log system alert.
        
        Args:
            alert (dict): Alert dictionary with level, message, and value
        """
        message = f"{alert['message']} - Value: {alert['value']}"
        self.log_event(message, alert['level'])
    
    def get_recent_logs(self, lines=10):
        """
        Get recent log entries.
        
        Args:
            lines (int): Number of recent lines to retrieve
            
        Returns:
            list: List of recent log entries
        """
        try:
            with open(self.log_file, 'r') as f:
                all_lines = f.readlines()
                return all_lines[-lines:] if all_lines else []
        except FileNotFoundError:
            return ["Log file not found"]
        except Exception as e:
            return [f"Error reading log file: {e}"]