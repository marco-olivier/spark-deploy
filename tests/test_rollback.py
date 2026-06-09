"""Rollback tests"""
import pytest
from spark_deploy.rollback import RollbackManager

class TestRollbackManager:
    def test_record_and_rollback(self):
        manager = RollbackManager()
        manager.record("app", "v1", 2)
        manager.record("app", "v2", 3)
        manager.record("app", "v3", 3)
        
        current = manager.get_current("app")
        assert current.image == "v3"
        
        previous = manager.rollback("app")
        assert previous.image == "v2"
    
    def test_history(self):
        manager = RollbackManager()
        manager.record("app", "v1", 1)
        manager.record("app", "v2", 2)
        
        history = manager.get_history("app")
        assert len(history) == 2
