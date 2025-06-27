"""
Main Window GUI Module
Simple Tkinter GUI for system monitoring display
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from daq.cpu import CPUMonitor
from daq.memory import MemoryMonitor
from daq.disk import DiskMonitor
from daq.temperature import TemperatureMonitor
from diagnostics.rules import DiagnosticRuleEngine
from logger.log_writer import SystemLogger

class SystemMonitorGUI:
    """Main GUI window for system monitoring application."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor - DAQ & DCS Demo")
        self.root.geometry("600x500")
        
        # Initialize components
        self.cpu_monitor = CPUMonitor()
        self.memory_monitor = MemoryMonitor()
        self.disk_monitor = DiskMonitor()
        self.temp_monitor = TemperatureMonitor()
        self.diagnostic_engine = DiagnosticRuleEngine()
        self.logger = SystemLogger()
        
        # GUI variables
        self.is_running = False
        
        self._create_widgets()
        self._start_monitoring()
    
    def _create_widgets(self):
        """Create and arrange GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # System status frame
        status_frame = ttk.LabelFrame(main_frame, text="System Status", padding="10")
        status_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # System parameters
        self.cpu_label = ttk.Label(status_frame, text="CPU: ---%", font=('Arial', 12))
        self.cpu_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        self.memory_label = ttk.Label(status_frame, text="Memory: ---%", font=('Arial', 12))
        self.memory_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        self.disk_label = ttk.Label(status_frame, text="Disk: ---%", font=('Arial', 12))
        self.disk_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 20), pady=(5, 0))
        
        self.temp_label = ttk.Label(status_frame, text="Temperature: ---°C", font=('Arial', 12))
        self.temp_label.grid(row=1, column=1, sticky=tk.W, padx=(0, 20), pady=(5, 0))
        
        # Health status
        health_frame = ttk.LabelFrame(main_frame, text="System Health", padding="10")
        health_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.health_label = ttk.Label(health_frame, text="Status: Checking...", 
                                     font=('Arial', 14, 'bold'), foreground='blue')
        self.health_label.grid(row=0, column=0, sticky=tk.W)
        
        # Alerts frame
        alerts_frame = ttk.LabelFrame(main_frame, text="Active Alerts", padding="10")
        alerts_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.alerts_text = scrolledtext.ScrolledText(alerts_frame, height=8, width=70)
        self.alerts_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="Stop Monitoring", 
                                      command=self._toggle_monitoring)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        refresh_button = ttk.Button(button_frame, text="Refresh Now", 
                                   command=self._update_display)
        refresh_button.grid(row=0, column=1)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        alerts_frame.columnconfigure(0, weight=1)
        alerts_frame.rowconfigure(0, weight=1)
    
    def _start_monitoring(self):
        """Start the monitoring loop."""
        self.is_running = True
        self._update_display()
    
    def _toggle_monitoring(self):
        """Toggle monitoring on/off."""
        self.is_running = not self.is_running
        if self.is_running:
            self.start_button.config(text="Stop Monitoring")
            self._update_display()
        else:
            self.start_button.config(text="Start Monitoring")
    
    def _update_display(self):
        """Update all display elements with current data."""
        if not self.is_running:
            return
        
        # Read data from all sensors
        cpu_usage = self.cpu_monitor.read_data()
        memory_usage = self.memory_monitor.read_data()
        disk_usage = self.disk_monitor.read_data()
        temperature = self.temp_monitor.read_data()
        
        # Update parameter labels
        self.cpu_label.config(text=f"CPU: {cpu_usage}%")
        self.memory_label.config(text=f"Memory: {memory_usage}%")
        self.disk_label.config(text=f"Disk: {disk_usage}%")
        self.temp_label.config(text=f"Temperature: {temperature}°C")
        
        # Get system health and alerts
        health_status = self.diagnostic_engine.get_system_health(
            cpu_usage, memory_usage, disk_usage, temperature)
        alerts = self.diagnostic_engine.evaluate_system(
            cpu_usage, memory_usage, disk_usage, temperature)
        
        # Update health status with color coding
        color_map = {'Healthy': 'green', 'Warning': 'orange', 'Critical': 'red'}
        self.health_label.config(
            text=f"Status: {health_status}", 
            foreground=color_map.get(health_status, 'blue')
        )
        
        # Update alerts display
        self.alerts_text.delete(1.0, tk.END)
        if alerts:
            for alert in alerts:
                alert_text = f"[{alert['level']}] {alert['message']} ({alert['value']})\n"
                self.alerts_text.insert(tk.END, alert_text)
                self.logger.log_alert(alert)
        else:
            self.alerts_text.insert(tk.END, "No active alerts - System operating normally\n")
        
        # Log system data
        self.logger.log_system_data(cpu_usage, memory_usage, disk_usage, temperature, health_status)
        
        # Schedule next update
        if self.is_running:
            self.root.after(2000, self._update_display)  # Update every 2 seconds