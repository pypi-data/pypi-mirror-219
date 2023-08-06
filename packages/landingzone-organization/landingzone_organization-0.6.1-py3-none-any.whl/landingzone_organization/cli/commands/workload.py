from typing import Optional
import click

from landingzone_organization.cli import Context


@click.group()
def cli():
    """Perform workload operations"""
    pass


@cli.command(name="list")
@click.pass_obj
@click.option("-l", "--location")
def list_workloads(ctx: Context, location: Optional[str]):
    """List all workloads"""
    locations = list(map(str.strip, location.split(","))) if location else []
    click.echo(f"Listing available workloads in: " + " > ".join(locations))

    for workload in ctx.organization.workloads(locations):
        click.echo(f"\nWorkload: {workload.name}")

        for account in workload.accounts:
            click.echo(f"\t{account.name} ({account.account_id})")
