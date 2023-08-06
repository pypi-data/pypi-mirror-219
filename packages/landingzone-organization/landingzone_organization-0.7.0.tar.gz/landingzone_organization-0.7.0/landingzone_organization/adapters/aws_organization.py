from typing import Iterator, List, Optional
import boto3

from landingzone_organization.account import Account
from landingzone_organization.organization import Organization
from landingzone_organization.organization_unit import OrganizationUnit


class AWSOrganization:
    def __init__(self, session: Optional[boto3.Session] = None) -> None:
        self.__client = (
            session.client("organizations")
            if session
            else boto3.client("organizations")
        )

    @property
    def root_id(self) -> str:
        paginator = self.__client.get_paginator("list_roots")
        response_iterator = paginator.paginate(
            PaginationConfig={"MaxItems": 1, "PageSize": 1}
        )

        def read_root_id(response: dict) -> Optional[str]:
            roots = response.get("Roots", {})
            return next(iter(roots)).get("Id")

        return next(map(read_root_id, response_iterator), None)  # type: ignore

    @staticmethod
    def __parse_response(response: Iterator, key: str) -> List[dict]:
        def flatten(input: List[List[dict]]) -> List[dict]:
            return [item for sublist in input for item in sublist]

        def read_iteration(response: dict) -> Optional[str]:
            return response.get(key)

        return flatten(map(read_iteration, response))  # type: ignore

    def __get_children(self, parent: str, child_type: str) -> List[str]:
        paginator = self.__client.get_paginator("list_children")
        response_iterator = paginator.paginate(
            ParentId=parent,
            ChildType=child_type,
        )
        response = self.__parse_response(response_iterator, "Children")
        return list(map(lambda x: x.get("Id"), response))  # type: ignore

    def __resolve_organization(self, parent: str) -> Organization:
        accounts = self.__get_children(parent, "ACCOUNT")
        ous = self.__get_children(parent, "ORGANIZATIONAL_UNIT")

        return Organization(
            id=parent,
            unit=OrganizationUnit(
                id=parent,
                name="Root",
                accounts=list(map(self.__resolve_account, accounts)),
                units=list(map(self.__resolve_organization_unit, ous)),
            ),
        )

    def __resolve_account(self, account_id: str) -> Account:
        account = self.__client.describe_account(AccountId=account_id).get(
            "Account", {}
        )
        return Account(name=account.get("Name"), account_id=account.get("Id"))

    def __resolve_organization_unit(
        self, organization_unit_id: str
    ) -> OrganizationUnit:
        unit = self.__client.describe_organizational_unit(
            OrganizationalUnitId=organization_unit_id
        ).get("OrganizationalUnit", {})
        accounts = self.__get_children(organization_unit_id, "ACCOUNT")
        ous = self.__get_children(organization_unit_id, "ORGANIZATIONAL_UNIT")

        return OrganizationUnit(
            id=unit.get("Id"),
            name=unit.get("Name"),
            accounts=list(map(self.__resolve_account, accounts)),
            units=list(map(self.__resolve_organization_unit, ous)),
        )

    def parse(self) -> Organization:
        return self.__resolve_organization(self.root_id)
