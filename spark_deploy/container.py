"""Container management"""
from typing import Optional, Dict, List
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ContainerConfig:
    """Container configuration"""
    base_image: str = "ubuntu:22.04"
    workdir: str = "/app"
    user: str = "root"
    env: Dict[str, str] = None
    
    def __post_init__(self):
        if self.env is None:
            self.env = {}

class Container:
    """Docker container management"""
    
    def __init__(self, name: str, config: Optional[ContainerConfig] = None):
        self.name = name
        self.config = config or ContainerConfig()
        self._dockerfile: Optional[str] = None
        self._built = False
    
    @classmethod
    def from_dockerfile(cls, path: str) -> 'Container':
        """Create from Dockerfile"""
        container = cls(name=Path(path).stem)
        container._dockerfile = path
        return container
    
    @classmethod
    def from_config(cls, name: str, config: ContainerConfig) -> 'Container':
        """Create from configuration"""
        return cls(name=name, config=config)
    
    def generate_dockerfile(self) -> str:
        """Generate Dockerfile content"""
        lines = [
            f"FROM {self.config.base_image}",
            f"WORKDIR {self.config.workdir}",
        ]
        for key, value in self.config.env.items():
            lines.append(f"ENV {key}={value}")
        lines.append("COPY . .")
        return "\n".join(lines)
    
    def build(self, tag: str, no_cache: bool = False) -> bool:
        """Build container image"""
        cmd = f"docker build -t {tag}"
        if no_cache:
            cmd += " --no-cache"
        if self._dockerfile:
            cmd += f" -f {self._dockerfile}"
        cmd += " ."
        
        import subprocess
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        self._built = result.returncode == 0
        return self._built
    
    def push(self, registry: str, tag: str) -> bool:
        """Push to registry"""
        full_tag = f"{registry}/{tag}"
        import subprocess
        result = subprocess.run(f"docker push {full_tag}", shell=True, capture_output=True)
        return result.returncode == 0
