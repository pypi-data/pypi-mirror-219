from __future__ import annotations

import os
import re
from typing import Optional

PATTERN_WORKLOAD_NAME = os.environ.get("PATTERN_WORKLOAD_NAME", ".*?-(.*)-.*")
PATTERN_ENVIRONMENT_NAME = os.environ.get("PATTERN_ENVIRONMENT_NAME", ".*-.*-(.*)")
ENVIRONMENT_WEIGHT = os.environ.get("ENVIRONMENT_WEIGHT", "dev,test,acc,prod")


def match_workload_pattern(name: str) -> bool:
    return bool(re.match(PATTERN_WORKLOAD_NAME, name))


def resolve_workload_name(name: str) -> Optional[str]:
    match = re.match(PATTERN_WORKLOAD_NAME, name)
    return match.group(1) if match else None


def resolve_account_environment(name: str) -> Optional[str]:
    match = re.match(PATTERN_ENVIRONMENT_NAME, name)
    return match.group(1) if match else None


def resolve_account_weight(name: str) -> int:
    order = ENVIRONMENT_WEIGHT.split(",")
    item = next(filter(lambda x: name.startswith(x), order), None)

    return order.index(item) if item else len(order)
