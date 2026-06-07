"""Configuration management"""
from typing import Optional, Dict, Any
from pathlib import Path
import yaml

class DeployConfig:
    """Deployment configuration"""
    
    def __init__(self):
        self.registry: str = ""
        self.namespace: str = "default"
        self.replicas: int = 1
        self.resources: Dict[str, str] = {}
        self.env: Dict[str, str] = {}
    
    @classmethod
    def from_file(cls, path: str) -> 'DeployConfig':
        """Load config from YAML file"""
        with open(path) as f:
            data = yaml.safe_load(f)
        
        config = cls()
        config.registry = data.get('registry', '')
        config.namespace = data.get('namespace', 'default')
        config.replicas = data.get('replicas', 1)
        config.resources = data.get('resources', {})
        config.env = data.get('env', {})
        return config
    
    @classmethod
    def from_env(cls) -> 'DeployConfig':
        """Load config from environment"""
        import os
        config = cls()
        config.registry = os.environ.get('DEPLOY_REGISTRY', '')
        config.namespace = os.environ.get('DEPLOY_NAMESPACE', 'default')
        return config
    
    def save(self, path: str):
        """Save config to file"""
        data = {
            'registry': self.registry,
            'namespace': self.namespace,
            'replicas': self.replicas,
            'resources': self.resources,
            'env': self.env,
        }
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
