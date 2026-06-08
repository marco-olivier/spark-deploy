"""Scaling tests"""
import pytest
from spark_deploy.scaling import AutoScaler
from spark_deploy.scaling.autoscaler import ScalingPolicy

class MockDeployer:
    def scale(self, name, replicas):
        return True

class TestAutoScaler:
    def test_scale_up(self):
        deployer = MockDeployer()
        policy = ScalingPolicy(scale_up_threshold=80)
        scaler = AutoScaler(deployer, policy)
        
        replicas = scaler.evaluate(90)
        assert replicas > 1
    
    def test_scale_down(self):
        deployer = MockDeployer()
        policy = ScalingPolicy(min_replicas=1, scale_down_threshold=20)
        scaler = AutoScaler(deployer, policy)
        scaler._current_replicas = 5
        
        replicas = scaler.evaluate(10)
        assert replicas < 5
