#!/usr/bin/env python3
"""
Simple System Monitor - Main Entry Point
Demonstrates DAQ, DCS principles, and GUI development
"""

import sys
import tkinter as tk
from gui.main_window import SystemMonitorGUI

def main():
    """Main entry point for the system monitor application."""
    root = tk.Tk()
    app = SystemMonitorGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nShutting down system monitor...")
        root.destroy()

if __name__ == "__main__":
    main()