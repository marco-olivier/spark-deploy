"""Kubernetes API client"""
from typing import Dict, Optional

class K8sClient:
    """Kubernetes API client wrapper"""
    
    def __init__(self, kubeconfig: str = None):
        self._kubeconfig = kubeconfig
        self._client = None
    
    def _connect(self):
        """Connect to cluster"""
        if self._client is None:
            try:
                from kubernetes import client, config
                if self._kubeconfig:
                    config.load_kube_config(config_file=self._kubeconfig)
                else:
                    config.load_incluster_config()
                self._client = client
            except ImportError:
                raise RuntimeError("kubernetes package not installed")
    
    def deploy(self, manifest: dict) -> bool:
        """Apply manifest to cluster"""
        self._connect()
        try:
            apps_v1 = self._client.AppsV1Api()
            if manifest['kind'] == 'Deployment':
                apps_v1.create_namespaced_deployment(
                    namespace="default",
                    body=manifest
                )
            return True
        except Exception as e:
            print(f"Deploy failed: {e}")
            return False
    
    def scale(self, name: str, replicas: int) -> bool:
        """Scale deployment"""
        self._connect()
        try:
            apps_v1 = self._client.AppsV1Api()
            apps_v1.patch_namespaced_deployment_scale(
                name=name,
                namespace="default",
                body={'spec': {'replicas': replicas}}
            )
            return True
        except Exception:
            return False
    
    def delete(self, name: str) -> bool:
        """Delete deployment"""
        self._connect()
        try:
            apps_v1 = self._client.AppsV1Api()
            apps_v1.delete_namespaced_deployment(
                name=name,
                namespace="default"
            )
            return True
        except Exception:
            return False
    
    def get_pods(self, label: str = None) -> list:
        """List pods"""
        self._connect()
        try:
            v1 = self._client.CoreV1Api()
            if label:
                pods = v1.list_namespaced_pod("default", label_selector=label)
            else:
                pods = v1.list_namespaced_pod("default")
            return [p.metadata.name for p in pods.items]
        except Exception:
            return []
