"""
Diagnostics Rules Module
Implements DCS-style rule-based diagnostics for system monitoring
"""

class DiagnosticRuleEngine:
    """Simple rule engine for system diagnostics and alerts."""
    
    def __init__(self):
        self.alerts = []
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self):
        """Initialize diagnostic rules for different system parameters."""
        return {
            'cpu_critical': {'threshold': 90, 'message': 'CPU usage critically high'},
            'memory_critical': {'threshold': 95, 'message': 'Memory usage critically high'},
            'disk_critical': {'threshold': 98, 'message': 'Disk space critically low'},
            'temp_critical': {'threshold': 85, 'message': 'System temperature too high'},
            'combined_load': {'cpu_threshold': 80, 'mem_threshold': 80, 
                            'message': 'High system load detected'}
        }
    
    def evaluate_system(self, cpu_usage, memory_usage, disk_usage, temperature):
        """
        Evaluate system state against diagnostic rules.
        
        Args:
            cpu_usage (float): CPU usage percentage
            memory_usage (float): Memory usage percentage  
            disk_usage (float): Disk usage percentage
            temperature (float): System temperature in Celsius
            
        Returns:
            list: List of active alerts
        """
        self.alerts.clear()
        
        # Individual parameter checks
        if cpu_usage >= self.rules['cpu_critical']['threshold']:
            self.alerts.append({
                'level': 'CRITICAL',
                'message': self.rules['cpu_critical']['message'],
                'value': cpu_usage
            })
        
        if memory_usage >= self.rules['memory_critical']['threshold']:
            self.alerts.append({
                'level': 'CRITICAL', 
                'message': self.rules['memory_critical']['message'],
                'value': memory_usage
            })
        
        if disk_usage >= self.rules['disk_critical']['threshold']:
            self.alerts.append({
                'level': 'CRITICAL',
                'message': self.rules['disk_critical']['message'], 
                'value': disk_usage
            })
        
        if temperature >= self.rules['temp_critical']['threshold']:
            self.alerts.append({
                'level': 'CRITICAL',
                'message': self.rules['temp_critical']['message'],
                'value': temperature
            })
        
        # Combined load check
        if (cpu_usage >= self.rules['combined_load']['cpu_threshold'] and 
            memory_usage >= self.rules['combined_load']['mem_threshold']):
            self.alerts.append({
                'level': 'WARNING',
                'message': self.rules['combined_load']['message'],
                'value': f"CPU: {cpu_usage}%, RAM: {memory_usage}%"
            })
        
        return self.alerts
    
    def get_system_health(self, cpu_usage, memory_usage, disk_usage, temperature):
        """
        Get overall system health status.
        
        Returns:
            str: Health status (Healthy, Warning, Critical)
        """
        alerts = self.evaluate_system(cpu_usage, memory_usage, disk_usage, temperature)
        
        if any(alert['level'] == 'CRITICAL' for alert in alerts):
            return 'Critical'
        elif alerts:
            return 'Warning'
        else:
            return 'Healthy'