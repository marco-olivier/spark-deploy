"""Health probes"""
from abc import ABC, abstractmethod
import subprocess
import socket

class Probe(ABC):
    """Base probe"""
    @abstractmethod
    def check(self) -> bool:
        pass

class HttpProbe(Probe):
    """HTTP health probe"""
    def __init__(self, url: str, timeout: int = 5):
        self.url = url
        self.timeout = timeout
    
    def check(self) -> bool:
        try:
            import requests
            response = requests.get(self.url, timeout=self.timeout)
            return response.status_code == 200
        except Exception:
            return False

class TcpProbe(Probe):
    """TCP health probe"""
    def __init__(self, host: str, port: int, timeout: int = 5):
        self.host = host
        self.port = port
        self.timeout = timeout
    
    def check(self) -> bool:
        try:
            sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
            sock.close()
            return True
        except Exception:
            return False

class CommandProbe(Probe):
    """Command health probe"""
    def __init__(self, command: str, timeout: int = 5):
        self.command = command
        self.timeout = timeout
    
    def check(self) -> bool:
        try:
            result = subprocess.run(
                self.command, shell=True,
                capture_output=True, timeout=self.timeout
            )
            return result.returncode == 0
        except Exception:
            return False
