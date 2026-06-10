# API Reference

## Pipeline

### `Pipeline(name="default")`
Create deployment pipeline.

### `pipeline.add_stage(name, func, **kwargs)`
Add pipeline stage.

### `pipeline.execute(context=None) -> bool`
Execute pipeline.

## Container

### `Container.from_dockerfile(path)`
Create from Dockerfile.

### `Container.from_config(name, config)`
Create from config.

### `container.build(tag, no_cache=False)`
Build image.

### `container.push(registry, tag)`
Push to registry.

## Deployer

### `Deployer(target=Docker)`
Create deployer.

### `deployer.deploy(name, image, replicas=1)`
Deploy container.

### `deployer.scale(name, replicas)`
Scale deployment.

### `deployer.rollback(name)`
Rollback deployment.

## ManifestBuilder

### `ManifestBuilder(name, image)`
Create K8s manifest builder.

### `builder.set_replicas(count)`
Set replica count.

### `builder.set_port(port)`
Set container port.

### `builder.to_yaml() -> str`
Generate YAML.
