from json import JSONDecodeError
from typing import Optional
import os
import boto3
import click
from boto3 import Session

from landingzone_organization.organization import Organization


class Context:
    def __init__(self, debug: bool, profile: Optional[str]) -> None:
        self.__debug = debug
        self.__profile = profile
        self.__organization: Optional[Organization] = None

    @property
    def session(self) -> Session:
        return boto3.session.Session(profile_name=self.__profile)

    @property
    def debug(self):
        return self.__debug

    @property
    def data_file(self):
        return os.path.join(os.getcwd(), "organization-data.json")

    @property
    def organization(self) -> Organization:
        if not self.__organization:
            try:
                with open(self.data_file, "r") as fh:
                    self.__organization = Organization.load(fh.read())
            except FileNotFoundError:
                click.echo(
                    "Please run `landingzone-organization organization download` first!"
                )
                raise click.Abort()
            except JSONDecodeError:
                click.echo(
                    "Source file has been corrupted, please run `landingzone-organization organization download` to recreate the file!"
                )
                raise click.Abort()
            except Exception as e:
                click.echo(e)
                raise click.Abort()

        return self.__organization
