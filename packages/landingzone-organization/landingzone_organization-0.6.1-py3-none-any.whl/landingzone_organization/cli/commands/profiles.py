import configparser
import os

import click

from landingzone_organization.cli import Context


@click.group()
def cli():
    """Perform profiles operations"""
    pass


@cli.command()
@click.argument("organization-name")
@click.option("--sso-start-url", prompt="SSO start URL")
@click.option("--sso-region", prompt="SSO region")
@click.option("--role-session-name", prompt="SSO session name")
@click.option("--sso-role-name", prompt="SSO role name")
@click.pass_obj
def generate(
    ctx: Context,
    organization_name: str,
    sso_start_url: str,
    sso_region: str,
    sso_role_name: str,
    role_session_name: str,
):
    """
    Generate the profiles that can be used by the AWS cli.

    AWS_CONFIG_FILE="~/.aws/config-acme" landingzone-organization profiles generate acme \
        --sso-start-url "https://acme.awsapps.com/start" \
        --sso-region "eu-central-1" \
        --role-session-name "John.Doe@acme.com" \
        --sso-role-name "my-sso-audit-role"
    """
    profiles = ctx.organization.sso_profiles(
        sso_start_url=sso_start_url,
        sso_region=sso_region,
        sso_role_name=sso_role_name,
        role_session_name=role_session_name,
    )

    parser = configparser.ConfigParser()

    for profile in profiles:
        section = f"profile {profile.account_name}"
        parser.add_section(section)
        parser.set(section, "sso_start_url", profile.sso_start_url)
        parser.set(section, "sso_region", profile.sso_region)
        parser.set(section, "sso_account_id", profile.account_id)
        parser.set(section, "sso_role_name", profile.sso_role_name)
        parser.set(section, "role_session_name", profile.role_session_name)

    file = os.environ.get(
        "AWS_CONFIG_FILE", os.path.join(os.getcwd(), f"{organization_name}.ini")
    )

    with open(os.path.expanduser(file), "w") as configfile:
        parser.write(configfile)

    click.echo(f"All profiles are written to {file}, you can now use:")
    click.echo("")
    click.echo(f"export AWS_CONFIG_FILE={file}")
    click.echo(f"aws s3 ls --profile <aws account name>")
