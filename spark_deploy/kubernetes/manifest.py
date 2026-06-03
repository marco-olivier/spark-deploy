"""Kubernetes manifest generation"""
from typing import Dict, List, Optional
import yaml

class ManifestBuilder:
    """Build Kubernetes manifests"""
    
    def __init__(self, name: str, image: str):
        self.name = name
        self.image = image
        self.replicas = 1
        self.port: Optional[int] = None
        self.env: Dict[str, str] = {}
        self.resources: Dict = {}
    
    def set_replicas(self, count: int) -> 'ManifestBuilder':
        self.replicas = count
        return self
    
    def set_port(self, port: int) -> 'ManifestBuilder':
        self.port = port
        return self
    
    def add_env(self, key: str, value: str) -> 'ManifestBuilder':
        self.env[key] = value
        return self
    
    def set_resources(self, cpu: str = "100m", memory: str = "128Mi") -> 'ManifestBuilder':
        self.resources = {
            'requests': {'cpu': cpu, 'memory': memory},
            'limits': {'cpu': cpu, 'memory': memory}
        }
        return self
    
    def build_deployment(self) -> dict:
        """Build deployment manifest"""
        containers = [{
            'name': self.name,
            'image': self.image,
        }]
        
        if self.port:
            containers[0]['ports'] = [{'containerPort': self.port}]
        
        if self.env:
            containers[0]['env'] = [
                {'name': k, 'value': v} for k, v in self.env.items()
            ]
        
        if self.resources:
            containers[0]['resources'] = self.resources
        
        return {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {'name': self.name},
            'spec': {
                'replicas': self.replicas,
                'selector': {'matchLabels': {'app': self.name}},
                'template': {
                    'metadata': {'labels': {'app': self.name}},
                    'spec': {'containers': containers}
                }
            }
        }
    
    def build_service(self) -> dict:
        """Build service manifest"""
        return {
            'apiVersion': 'v1',
            'kind': 'Service',
            'metadata': {'name': self.name},
            'spec': {
                'selector': {'app': self.name},
                'ports': [{'port': self.port or 80}],
                'type': 'ClusterIP'
            }
        }
    
    def to_yaml(self) -> str:
        """Generate YAML output"""
        deployment = self.build_deployment()
        return yaml.dump(deployment, default_flow_style=False)
    
    def write(self, path: str):
        """Write manifest to file"""
        with open(path, 'w') as f:
            f.write(self.to_yaml())
