#  Copyright (c) 2023 Roboto Technologies, Inc.

import collections.abc
from typing import Any, Optional

from ...domain.actions import ActionDelegate
from ...serde import pydantic_jsonable_dict
from .trigger_delegate import TriggerDelegate
from .trigger_record import TriggerRecord


class Trigger:
    __record: TriggerRecord
    __action_delegate: ActionDelegate
    __trigger_delegate: TriggerDelegate

    @classmethod
    def create(
        cls,
        name: str,
        org_id: Optional[str],
        action_name: str,
        action_delegate: ActionDelegate,
        trigger_delegate: TriggerDelegate,
    ) -> "Trigger":
        record = trigger_delegate.create_trigger(
            name=name, org_id=org_id, action_name=action_name
        )
        return cls(
            record=record,
            action_delegate=action_delegate,
            trigger_delegate=trigger_delegate,
        )

    # And version?
    @classmethod
    def from_name(
        cls,
        name: str,
        org_id: Optional[str],
        action_delegate: ActionDelegate,
        trigger_delegate: TriggerDelegate,
    ) -> "Trigger":
        record = trigger_delegate.get_trigger_by_primary_key(name=name, org_id=org_id)
        return cls(
            record=record,
            action_delegate=action_delegate,
            trigger_delegate=trigger_delegate,
        )

    @classmethod
    def query(
        cls,
        filters: Optional[dict[str, Any]],
        org_id: Optional[str],
        action_delegate: ActionDelegate,
        trigger_delegate: TriggerDelegate,
    ) -> collections.abc.Generator["Trigger", None, None]:
        paginated_results = trigger_delegate.query_triggers(
            filters=filters, org_id=org_id
        )
        while True:
            for record in paginated_results.items:
                yield cls(
                    record=record,
                    action_delegate=action_delegate,
                    trigger_delegate=trigger_delegate,
                )
            if paginated_results.next_token:
                paginated_results = trigger_delegate.query_triggers(
                    filters=filters,
                    org_id=org_id,
                    page_token=paginated_results.next_token,
                )
            else:
                break

    def __init__(
        self,
        record: TriggerRecord,
        action_delegate: ActionDelegate,
        trigger_delegate: TriggerDelegate,
    ):
        self.__record = record
        self.__action_delegate = action_delegate
        self.__trigger_delegate = trigger_delegate

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)
