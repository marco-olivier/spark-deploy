#!/usr/bin/env python3
"""Kubernetes deployment example"""
from spark_deploy.kubernetes import ManifestBuilder

def main():
    # Build manifest
    builder = ManifestBuilder("compute-service", "compute:latest")
    builder.set_replicas(3)
    builder.set_port(8080)
    builder.set_resources(cpu="500m", memory="512Mi")
    builder.add_env("LOG_LEVEL", "info")
    
    # Generate YAML
    yaml = builder.to_yaml()
    print(yaml)
    
    # Write to file
    builder.write("deployment.yaml")
    print("Written to deployment.yaml")

if __name__ == "__main__":
    main()
