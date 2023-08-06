from __future__ import annotations

from typing import List
from dataclasses import dataclass, field
from landingzone_organization.account import Account


@dataclass
class OrganizationUnit:
    """
    Understands organization units
    """

    id: str
    name: str
    accounts: List[Account] = field(default_factory=list)
    units: List[OrganizationUnit] = field(default_factory=list)

    @property
    def has_accounts(self) -> bool:
        return len(self.accounts) > 0

    @property
    def accounts_recursive(self) -> List[Account]:
        result = []

        for unit in self.units:
            result.extend(unit.accounts_recursive)

        result.extend(self.accounts)

        return result

    def by_name(self, name: str) -> OrganizationUnit:
        def name_matches(unit: OrganizationUnit) -> bool:
            return unit.name == name

        return next(filter(name_matches, self.units), None)  # type: ignore
