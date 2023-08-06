from typing import List, Dict, Callable
import configparser
import boto3
import botocore


class Profiles:
    def __init__(self, config_file: str):
        self.__config_file = config_file
        self.__config = configparser.ConfigParser()
        self.__config.read(config_file)
        self.__client_errors = {}

    @property
    def names(self) -> List[str]:
        def extract_profile_name(section: str) -> str:
            return section.split(" ")[-1]

        return list(map(extract_profile_name, self.__config.sections()))

    def execute(
        self, regions: List[str], callback: Callable[[boto3.session.Session, str], None]
    ):
        self.__client_errors = {}

        for profile in self.names:
            session = boto3.session.Session(profile_name=profile)

            for region in regions:
                try:
                    callback(session, region)
                except botocore.exceptions.ClientError as exception:
                    self.__client_errors[f"{profile}-{region}"] = exception

    @property
    def client_exceptions(self) -> Dict[str, botocore.exceptions.ClientError]:
        return self.__client_errors
