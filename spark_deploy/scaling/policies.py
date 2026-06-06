"""Scaling policies"""
from typing import List
from abc import ABC, abstractmethod
import numpy as np

class ScalingPolicyBase(ABC):
    """Base scaling policy"""
    @abstractmethod
    def should_scale(self, metrics: List[float]) -> tuple:
        pass

class ThresholdPolicy(ScalingPolicyBase):
    """Simple threshold-based scaling"""
    def __init__(self, scale_up: float = 80, scale_down: float = 20):
        self.scale_up = scale_up
        self.scale_down = scale_down
    
    def should_scale(self, metrics: List[float]) -> tuple:
        if not metrics:
            return (0, 0)
        avg = np.mean(metrics[-5:])  # Last 5 samples
        if avg > self.scale_up:
            return (1, avg)  # Scale up
        elif avg < self.scale_down:
            return (-1, avg)  # Scale down
        return (0, avg)

class PercentilePolicy(ScalingPolicyBase):
    """Percentile-based scaling"""
    def __init__(self, scale_up_percentile: float = 95, threshold: float = 80):
        self.scale_up_percentile = scale_up_percentile
        self.threshold = threshold
    
    def should_scale(self, metrics: List[float]) -> tuple:
        if not metrics:
            return (0, 0)
        p95 = np.percentile(metrics, self.scale_up_percentile)
        if p95 > self.threshold:
            return (1, p95)
        return (0, p95)
