#!/usr/bin/env python3
"""Basic deployment example"""
from spark_deploy import Pipeline, Container

def build_step(ctx):
    container = Container.from_dockerfile("Dockerfile")
    container.build(tag="myapp:latest")
    return {"image": "myapp:latest"}

def test_step(ctx):
    print("Running tests...")
    return {"tests_passed": True}

def deploy_step(ctx):
    from spark_deploy import Deployer
    deployer = Deployer()
    deployer.deploy("myapp", ctx["image"])
    return {"deployed": True}

def main():
    pipeline = Pipeline("deploy")
    pipeline.add_stage("build", build_step)
    pipeline.add_stage("test", test_step)
    pipeline.add_stage("deploy", deploy_step)
    
    success = pipeline.execute()
    print(f"Pipeline {'succeeded' if success else 'failed'}")

if __name__ == "__main__":
    main()
