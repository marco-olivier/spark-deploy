from setuptools import setup, find_packages

setup(
    name="spark-deploy",
    version="0.1.0",
    author="Marco Olivier",
    description="Deployment pipeline and container orchestration",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=["docker>=6.0", "pyyaml>=6.0", "click>=8.0"],
    extras_require={"k8s": ["kubernetes>=25.0"], "dev": ["pytest"]},
)
