import csv
from typing import List

import click

from landingzone_organization import Account
from landingzone_organization.cli import Context


@click.group()
def cli():
    """Perform account operations"""
    pass


@cli.command()
@click.argument("account-id")
@click.pass_obj
def view(ctx: Context, account_id: str):
    """List all workloads"""
    account = ctx.organization.by_account_id(account_id)

    if account:
        click.echo(f"Account ID  : {account.account_id}")
        click.echo(f"Name        : {account.name}")
        click.echo(f"Environment : {account.environment}")
    else:
        click.echo(f"The {account_id} is not known to this organization.")


@cli.command()
@click.argument("output")
@click.pass_obj
def export(ctx: Context, output: str):
    """List all workloads"""
    perform_export(output, ctx.organization.accounts([]))


def perform_export(path: str, accounts: List[Account]) -> None:
    with open(path, "w") as fh:
        writer = csv.writer(fh, delimiter=";", quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["AccountId", "Name", "Environment"])

    for account in accounts:
        writer.writerow([account.account_id, account.name, account.environment])
