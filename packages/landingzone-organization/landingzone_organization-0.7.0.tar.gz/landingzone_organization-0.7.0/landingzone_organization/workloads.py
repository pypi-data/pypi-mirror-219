from __future__ import annotations
from typing import List, Optional, Set

from landingzone_organization.account import Account
from landingzone_organization.workload import Workload
from landingzone_organization.filtering import resolve_workload_name


class Workloads:
    def __init__(self, workloads: List[Workload]) -> None:
        self.__index = 0
        self.__workloads = workloads

    def __len__(self) -> int:
        return len(self.__workloads)

    def __iter__(self):
        for workload in self.__workloads:
            yield workload

    @property
    def names(self) -> Set[str]:
        return set(map(lambda workload: workload.name, self.__workloads))

    @property
    def accounts(self) -> List[Account]:
        accounts = []

        for workload in self.__workloads:
            accounts.extend(workload.accounts)

        return accounts

    @property
    def environments(self) -> Set[str]:
        environments = set()

        for workload in self.__workloads:
            environments.update(workload.environments)

        return environments

    def resolve_account(self, account: Account) -> None:
        workload_name = resolve_workload_name(account.name)
        workload = self.by_name(workload_name)

        if not workload:
            self.__workloads.append(Workload(name=workload_name, accounts=[account]))
        else:
            workload.append(account)

    def by_name(self, name: str) -> Optional[Workload]:
        return next(filter(lambda w: w.name == name, self.__workloads), None)  # type: ignore
