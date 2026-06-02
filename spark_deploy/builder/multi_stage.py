"""Multi-stage Docker builds"""
from typing import List
from .dockerfile import DockerfileBuilder

class Stage:
    """Build stage"""
    def __init__(self, name: str, base_image: str):
        self.name = name
        self.base_image = base_image
        self._builder = DockerfileBuilder(base_image)
    
    def __getattr__(self, name):
        return getattr(self._builder, name)

class MultiStageBuilder:
    """Multi-stage Dockerfile builder"""
    
    def __init__(self):
        self._stages: List[Stage] = []
        self._final_instructions: List[str] = []
    
    def add_stage(self, name: str, base_image: str) -> Stage:
        """Add build stage"""
        stage = Stage(name, base_image)
        self._stages.append(stage)
        return stage
    
    def final_from(self, image: str):
        """Set final stage base"""
        self._final_instructions.append(f"FROM {image}")
    
    def final_copy(self, src: str, dest: str, from_stage: str = ""):
        """Copy from previous stage"""
        if from_stage:
            self._final_instructions.append(f"COPY --from={from_stage} {src} {dest}")
        else:
            self._final_instructions.append(f"COPY {src} {dest}")
    
    def build(self) -> str:
        """Generate multi-stage Dockerfile"""
        lines = []
        for stage in self._stages:
            lines.append(f"# Stage: {stage.name}")
            lines.append(stage._builder.build())
            lines.append("")
        
        lines.append("# Final stage")
        lines.extend(self._final_instructions)
        return "\n".join(lines)
