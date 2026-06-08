"""Container tests"""
import pytest
from spark_deploy.container import Container, ContainerConfig

class TestContainer:
    def test_from_config(self):
        config = ContainerConfig(base_image="python:3.11")
        container = Container.from_config("test", config)
        assert container.name == "test"
    
    def test_generate_dockerfile(self):
        config = ContainerConfig(base_image="ubuntu:22.04")
        container = Container.from_config("test", config)
        dockerfile = container.generate_dockerfile()
        assert "FROM ubuntu:22.04" in dockerfile
