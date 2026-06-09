"""Manifest tests"""
import pytest
from spark_deploy.kubernetes import ManifestBuilder

class TestManifestBuilder:
    def test_deployment(self):
        builder = ManifestBuilder("test-app", "nginx:latest")
        builder.set_replicas(3)
        builder.set_port(80)
        manifest = builder.build_deployment()
        assert manifest['kind'] == 'Deployment'
        assert manifest['spec']['replicas'] == 3
    
    def test_service(self):
        builder = ManifestBuilder("test-app", "nginx:latest")
        builder.set_port(80)
        service = builder.build_service()
        assert service['kind'] == 'Service'
