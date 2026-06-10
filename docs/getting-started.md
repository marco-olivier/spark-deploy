# Getting Started

## Installation

```bash
pip install spark-deploy
```

## Basic Usage

```python
from spark_deploy import Pipeline, Container

# Create pipeline
pipeline = Pipeline()

# Add stages
pipeline.add_stage("build", build_func)
pipeline.add_stage("deploy", deploy_func)

# Execute
pipeline.execute()
```

## Container Building

```python
from spark_deploy.builder import DockerfileBuilder

builder = DockerfileBuilder("python:3.11")
builder.workdir("/app")
builder.copy(".", ".")
builder.run("pip install -r requirements.txt")
builder.write("Dockerfile")
```
