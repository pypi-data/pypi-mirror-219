#  Copyright (c) 2023 Roboto Technologies, Inc.

import abc
from typing import Any, Optional

from ...pagination import PaginatedList
from .trigger_record import TriggerRecord


class TriggerDelegate(abc.ABC):
    @abc.abstractmethod
    def create_trigger(
        self, name: str, org_id: Optional[str], action_name: str
    ) -> TriggerRecord:
        raise NotImplementedError("create_trigger")

    @abc.abstractmethod
    def get_trigger_by_primary_key(
        self, name: str, org_id: Optional[str]
    ) -> TriggerRecord:
        raise NotImplementedError("get_trigger_by_primary_key")

    @abc.abstractmethod
    def query_triggers(
        self,
        filters: Optional[dict[str, Any]],
        org_id: Optional[str],
        page_token: Optional[dict[str, str]] = None,
    ) -> PaginatedList[TriggerRecord]:
        raise NotImplementedError("get_triggers_for_org")
