"""Dockerfile generation"""
from typing import List, Dict

class DockerfileBuilder:
    """Build Dockerfiles programmatically"""
    
    def __init__(self, base_image: str = "ubuntu:22.04"):
        self._base = base_image
        self._instructions: List[str] = [f"FROM {base_image}"]
    
    def workdir(self, path: str) -> 'DockerfileBuilder':
        self._instructions.append(f"WORKDIR {path}")
        return self
    
    def run(self, command: str) -> 'DockerfileBuilder':
        self._instructions.append(f"RUN {command}")
        return self
    
    def copy(self, src: str, dest: str) -> 'DockerfileBuilder':
        self._instructions.append(f"COPY {src} {dest}")
        return self
    
    def env(self, key: str, value: str) -> 'DockerfileBuilder':
        self._instructions.append(f"ENV {key}={value}")
        return self
    
    def expose(self, port: int) -> 'DockerfileBuilder':
        self._instructions.append(f"EXPOSE {port}")
        return self
    
    def cmd(self, command: str) -> 'DockerfileBuilder':
        self._instructions.append(f'CMD ["{command}"]')
        return self
    
    def entrypoint(self, command: str) -> 'DockerfileBuilder':
        self._instructions.append(f'ENTRYPOINT ["{command}"]')
        return self
    
    def build(self) -> str:
        """Generate Dockerfile content"""
        return "\n".join(self._instructions)
    
    def write(self, path: str):
        """Write Dockerfile to file"""
        with open(path, 'w') as f:
            f.write(self.build())
