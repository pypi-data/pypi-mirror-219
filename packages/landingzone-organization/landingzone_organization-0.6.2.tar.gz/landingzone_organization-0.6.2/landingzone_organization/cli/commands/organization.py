import click
from landingzone_organization.adapters import AWSOrganization
from landingzone_organization.cli import Context


@click.group()
def cli():
    """Perform organization operations"""
    pass


@cli.command()
@click.pass_obj
def download(ctx: Context):
    """Download the organization structure"""
    click.echo(f"Download organization information")
    organization = AWSOrganization(ctx.session).parse()

    with open(ctx.data_file, "w") as fh:
        fh.write(organization.dump())

    click.echo(f"Content downloaded to: {ctx.data_file}")
