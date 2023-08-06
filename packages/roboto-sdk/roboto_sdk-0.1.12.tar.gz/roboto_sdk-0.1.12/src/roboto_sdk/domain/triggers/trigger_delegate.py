#  Copyright (c) 2023 Roboto Technologies, Inc.

import abc
from typing import Any, Optional

from ...pagination import PaginatedList
from ..actions import (
    ComputeRequirements,
    ContainerParameters,
)
from .trigger_record import TriggerRecord


class TriggerDelegate(abc.ABC):
    @abc.abstractmethod
    def create_trigger(
        self,
        name: str,
        action_name: str,
        required_inputs: list[str],
        org_id: Optional[str] = None,
        compute_requirement_overrides: Optional[ComputeRequirements] = None,
        container_parameter_overrides: Optional[ContainerParameters] = None,
    ) -> TriggerRecord:
        raise NotImplementedError("create_trigger")

    @abc.abstractmethod
    def get_trigger_by_primary_key(
        self, name: str, org_id: Optional[str] = None
    ) -> TriggerRecord:
        raise NotImplementedError("get_trigger_by_primary_key")

    @abc.abstractmethod
    def query_triggers(
        self,
        filters: Optional[dict[str, Any]],
        org_id: Optional[str] = None,
        page_token: Optional[dict[str, str]] = None,
    ) -> PaginatedList[TriggerRecord]:
        raise NotImplementedError("get_triggers_for_org")

    @abc.abstractmethod
    def delete_trigger(self, name: str, org_id: str) -> None:
        raise NotImplementedError("delete_trigger")
