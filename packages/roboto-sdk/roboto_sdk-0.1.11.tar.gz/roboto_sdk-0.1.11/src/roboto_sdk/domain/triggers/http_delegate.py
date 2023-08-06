#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Any, Optional

from ...http import (
    ORG_OVERRIDE_HEADER,
    HttpClient,
)
from ...pagination import PaginatedList
from ...serde import pydantic_jsonable_dict
from .http_resources import CreateTriggerRequest
from .trigger_delegate import TriggerDelegate
from .trigger_record import TriggerRecord


class TriggerHttpDelegate(TriggerDelegate):
    __http_client: HttpClient

    def __init__(self, http_client: HttpClient):
        super().__init__()
        self.__http_client = http_client

    def create_trigger(
        self, name: str, org_id: Optional[str], action_name: str
    ) -> TriggerRecord:
        url = self.__http_client.url("v1/triggers")
        headers = {"Content-Type": "application/json"}
        if org_id is not None:
            headers[ORG_OVERRIDE_HEADER] = org_id

        request_body = CreateTriggerRequest(name=name, action_name=action_name)

        response = self.__http_client.post(
            url, data=pydantic_jsonable_dict(request_body), headers=headers
        )
        return TriggerRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_trigger_by_primary_key(
        self, name: str, org_id: Optional[str]
    ) -> TriggerRecord:
        url = self.__http_client.url(f"v1/triggers/{name}")
        headers = {}
        if org_id is not None:
            headers[ORG_OVERRIDE_HEADER] = org_id
        response = self.__http_client.get(url, headers=headers)
        return TriggerRecord.parse_obj(response.from_json(json_path=["data"]))

    def query_triggers(
        self,
        filters: Optional[dict[str, Any]],
        org_id: Optional[str],
        page_token: Optional[dict[str, str]] = None,
    ) -> PaginatedList[TriggerRecord]:
        url = self.__http_client.url("v1/triggers")

        headers = {}
        if org_id is not None:
            headers = {ORG_OVERRIDE_HEADER: org_id}

        response = self.__http_client.get(url, headers=headers)
        unmarshalled = response.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                TriggerRecord.parse_obj(trigger) for trigger in unmarshalled["items"]
            ],
            next_token=unmarshalled.get("next_token", None),
        )
