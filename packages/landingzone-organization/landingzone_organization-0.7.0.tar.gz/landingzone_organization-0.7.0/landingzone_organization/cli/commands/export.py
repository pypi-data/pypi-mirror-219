import configparser
import os

import click

from landingzone_organization import Workload
from landingzone_organization.cli import Context
from landingzone_organization.workload_generator import WorkloadGenerator


@click.group()
def cli():
    """Perform profiles operations"""
    pass


@cli.command()
@click.argument("config-path")
@click.argument("ou-path")
@click.pass_obj
def workloads(ctx: Context, config_path: str, ou_path: str) -> None:
    """
    Export the workloads in the supplied path
    """
    ctx.info("Prepare the folder structure based on the organisation structure")
    workloads = ctx.organization.workloads(ou_path.split("/"))
    ctx.debug(f"\tFound {len(workloads)} workloads")

    def handle_workload(workload: Workload) -> None:
        WorkloadGenerator(config_path=config_path, workload=workload).execute()

    list(map(handle_workload, workloads))
