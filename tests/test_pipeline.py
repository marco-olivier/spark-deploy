"""Pipeline tests"""
import pytest
from spark_deploy.pipeline import Pipeline, StageStatus

class TestPipeline:
    def test_execute(self):
        def stage1(ctx):
            return {"result": 42}
        
        pipeline = Pipeline("test")
        pipeline.add_stage("s1", stage1)
        result = pipeline.execute()
        assert result == True
    
    def test_failure(self):
        def failing_stage(ctx):
            raise ValueError("Failed")
        
        pipeline = Pipeline("test")
        pipeline.add_stage("fail", failing_stage)
        result = pipeline.execute()
        assert result == False
        assert pipeline.has_failed
