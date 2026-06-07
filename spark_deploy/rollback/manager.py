"""Rollback manager"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import time

@dataclass
class DeploymentVersion:
    """Deployment version record"""
    name: str
    image: str
    timestamp: float
    replicas: int

class RollbackManager:
    """Manage deployment versions and rollbacks"""
    
    def __init__(self):
        self._versions: Dict[str, List[DeploymentVersion]] = {}
        self._current: Dict[str, DeploymentVersion] = {}
    
    def record(self, name: str, image: str, replicas: int):
        """Record deployment version"""
        version = DeploymentVersion(
            name=name,
            image=image,
            timestamp=time.time(),
            replicas=replicas
        )
        
        if name not in self._versions:
            self._versions[name] = []
        self._versions[name].append(version)
        self._current[name] = version
    
    def rollback(self, name: str, steps: int = 1) -> Optional[DeploymentVersion]:
        """Rollback to previous version"""
        if name not in self._versions:
            return None
        
        versions = self._versions[name]
        if len(versions) < steps + 1:
            return None
        
        target = versions[-(steps + 1)]
        self._current[name] = target
        return target
    
    def get_current(self, name: str) -> Optional[DeploymentVersion]:
        """Get current version"""
        return self._current.get(name)
    
    def get_history(self, name: str) -> List[DeploymentVersion]:
        """Get deployment history"""
        return self._versions.get(name, [])
    
    def compare(self, name: str, version1: int, version2: int) -> dict:
        """Compare two versions"""
        versions = self._versions.get(name, [])
        if version1 >= len(versions) or version2 >= len(versions):
            return {}
        
        v1 = versions[version1]
        v2 = versions[version2]
        
        return {
            'image_changed': v1.image != v2.image,
            'replicas_changed': v1.replicas != v2.replicas,
            'v1': {'image': v1.image, 'replicas': v1.replicas},
            'v2': {'image': v2.image, 'replicas': v2.replicas},
        }
