# Deployment Guide

## Docker Deployment

```python
from spark_deploy import Deployer

deployer = Deployer(target="docker")
deployer.deploy("my-app", "my-app:latest", replicas=1)
```

## Kubernetes Deployment

```python
from spark_deploy import Deployer
from spark_deploy.kubernetes import ManifestBuilder

# Build manifest
manifest = ManifestBuilder("my-app", "my-app:latest")
manifest.set_replicas(3)
manifest.set_port(8080)
manifest.write("deploy.yaml")

# Deploy
deployer = Deployer(target="kubernetes")
deployer.deploy("my-app", "my-app:latest", replicas=3)
```

## Auto-scaling

```python
from spark_deploy.scaling import AutoScaler

scaler = AutoScaler(deployer, policy=ScalingPolicy(
    min_replicas=1,
    max_replicas=10,
    scale_up_threshold=80
))

# In monitoring loop
replicas = scaler.evaluate(cpu_usage)
scaler.scale("my-app", replicas)
```

## Rollback

```python
from spark_deploy.rollback import RollbackManager

manager = RollbackManager()
manager.record("app", "v1", 2)
manager.record("app", "v2", 3)

# Rollback to v1
previous = manager.rollback("app", steps=1)
```
