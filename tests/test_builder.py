"""Builder tests"""
import pytest
from spark_deploy.builder import DockerfileBuilder

class TestDockerfileBuilder:
    def test_basic_build(self):
        builder = DockerfileBuilder("python:3.11")
        builder.workdir("/app")
        builder.copy(".", ".")
        builder.run("pip install -r requirements.txt")
        result = builder.build()
        assert "FROM python:3.11" in result
        assert "WORKDIR /app" in result
    
    def test_expose(self):
        builder = DockerfileBuilder()
        builder.expose(8080)
        result = builder.build()
        assert "EXPOSE 8080" in result
