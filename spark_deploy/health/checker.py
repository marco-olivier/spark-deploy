"""Health checker"""
from typing import List, Dict, Optional
from enum import Enum
import time

class HealthStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

class HealthChecker:
    """Check service health"""
    
    def __init__(self):
        self._checks: List[dict] = []
        self._results: Dict[str, HealthStatus] = {}
    
    def add_http_check(self, name: str, url: str, interval: int = 30):
        """Add HTTP health check"""
        self._checks.append({
            'name': name,
            'type': 'http',
            'url': url,
            'interval': interval
        })
    
    def add_tcp_check(self, name: str, host: str, port: int, interval: int = 30):
        """Add TCP health check"""
        self._checks.append({
            'name': name,
            'type': 'tcp',
            'host': host,
            'port': port,
            'interval': interval
        })
    
    def check_all(self) -> Dict[str, HealthStatus]:
        """Run all health checks"""
        for check in self._checks:
            try:
                if check['type'] == 'http':
                    self._results[check['name']] = self._check_http(check['url'])
                elif check['type'] == 'tcp':
                    self._results[check['name']] = self._check_tcp(check['host'], check['port'])
            except Exception:
                self._results[check['name']] = HealthStatus.UNHEALTHY
        
        return self._results
    
    def _check_http(self, url: str) -> HealthStatus:
        """Check HTTP endpoint"""
        try:
            import requests
            response = requests.get(url, timeout=5)
            return HealthStatus.HEALTHY if response.status_code == 200 else HealthStatus.UNHEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY
    
    def _check_tcp(self, host: str, port: int) -> HealthStatus:
        """Check TCP connection"""
        import socket
        try:
            sock = socket.create_connection((host, port), timeout=5)
            sock.close()
            return HealthStatus.HEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY
    
    @property
    def is_healthy(self) -> bool:
        return all(s == HealthStatus.HEALTHY for s in self._results.values())
