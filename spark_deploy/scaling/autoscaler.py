"""Auto-scaler"""
from typing import Optional, Callable
from dataclasses import dataclass

@dataclass
class ScalingPolicy:
    """Scaling configuration"""
    min_replicas: int = 1
    max_replicas: int = 10
    scale_up_threshold: float = 80.0
    scale_down_threshold: float = 20.0
    cooldown_seconds: int = 300

class AutoScaler:
    """Automatic scaling based on metrics"""
    
    def __init__(self, deployer: 'Deployer', policy: Optional[ScalingPolicy] = None):
        self.deployer = deployer
        self.policy = policy or ScalingPolicy()
        self._current_replicas = self.policy.min_replicas
        self._last_scale_time = 0
    
    def evaluate(self, metric_value: float) -> int:
        """Evaluate scaling decision"""
        import time
        now = time.time()
        
        if now - self._last_scale_time < self.policy.cooldown_seconds:
            return self._current_replicas
        
        if metric_value > self.policy.scale_up_threshold:
            new_replicas = min(self._current_replicas + 1, self.policy.max_replicas)
        elif metric_value < self.policy.scale_down_threshold:
            new_replicas = max(self._current_replicas - 1, self.policy.min_replicas)
        else:
            return self._current_replicas
        
        if new_replicas != self._current_replicas:
            self._current_replicas = new_replicas
            self._last_scale_time = now
        
        return self._current_replicas
    
    def scale(self, name: str, replicas: int) -> bool:
        """Scale deployment"""
        return self.deployer.scale(name, replicas)
    
    @property
    def current_replicas(self) -> int:
        return self._current_replicas
