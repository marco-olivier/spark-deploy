"""Command-line interface"""
import click

@click.group()
def cli():
    """Spark Deploy CLI"""
    pass

@cli.command()
@click.option("--file", "-f", default="Dockerfile", help="Dockerfile path")
@click.option("--tag", "-t", required=True, help="Image tag")
def build(file, tag):
    """Build container image"""
    from spark_deploy.container import Container
    container = Container.from_dockerfile(file)
    container.build(tag=tag)
    click.echo(f"Built: {tag}")

@cli.command()
@click.option("--name", "-n", required=True, help="Deployment name")
@click.option("--image", "-i", required=True, help="Container image")
@click.option("--replicas", "-r", default=1, help="Number of replicas")
def deploy(name, image, replicas):
    """Deploy container"""
    from spark_deploy.deployer import Deployer
    deployer = Deployer()
    deployer.deploy(name, image, replicas)
    click.echo(f"Deployed: {name}")

@cli.command()
def status():
    """Show deployment status"""
    click.echo("No active deployments")

if __name__ == "__main__":
    cli()
