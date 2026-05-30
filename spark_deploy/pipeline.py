"""Deployment pipeline"""
from typing import List, Callable, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import time

class StageStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class Stage:
    """Pipeline stage"""
    name: str
    func: Callable
    args: dict = field(default_factory=dict)
    status: StageStatus = StageStatus.PENDING
    duration: float = 0
    error: Optional[str] = None

class Pipeline:
    """Deployment pipeline"""
    
    def __init__(self, name: str = "default"):
        self.name = name
        self._stages: List[Stage] = []
        self._context: dict = {}
    
    def add_stage(self, name: str, func: Callable, **kwargs) -> 'Pipeline':
        """Add pipeline stage"""
        self._stages.append(Stage(name=name, func=func, args=kwargs))
        return self
    
    def execute(self, context: dict = None) -> bool:
        """Execute pipeline"""
        self._context = context or {}
        
        for stage in self._stages:
            stage.status = StageStatus.RUNNING
            start = time.time()
            
            try:
                result = stage.func(self._context, **stage.args)
                if isinstance(result, dict):
                    self._context.update(result)
                stage.status = StageStatus.SUCCESS
                stage.duration = time.time() - start
            except Exception as e:
                stage.status = StageStatus.FAILED
                stage.error = str(e)
                stage.duration = time.time() - start
                return False
        
        return True
    
    def get_status(self) -> List[dict]:
        """Get pipeline status"""
        return [
            {'name': s.name, 'status': s.status.value, 'duration': s.duration}
            for s in self._stages
        ]
    
    @property
    def is_complete(self) -> bool:
        return all(s.status == StageStatus.SUCCESS for s in self._stages)
    
    @property
    def has_failed(self) -> bool:
        return any(s.status == StageStatus.FAILED for s in self._stages)
