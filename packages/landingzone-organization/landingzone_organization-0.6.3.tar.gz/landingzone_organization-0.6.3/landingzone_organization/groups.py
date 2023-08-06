from __future__ import annotations
from typing import List, Optional
from dataclasses import dataclass
from landingzone_organization.organization import Organization
from landingzone_organization.group import Group


@dataclass
class Groups:
    """
    Understands what groups are available within the landingzone
    """

    groups: List[Group]
    organization: Optional[Organization] = None

    def __post_init__(self):
        def pass_organization(group: Group) -> None:
            if self.organization:
                group.organization(self.organization)

        list(map(pass_organization, self.groups))

    def valid_group(self, name: str) -> bool:
        return self.by_name(name) is not None

    def by_name(self, name: str) -> Optional[Group]:
        def name_matches(group: Group) -> bool:
            return group.name == name

        return next(filter(name_matches, self.groups), None)  # type: ignore
