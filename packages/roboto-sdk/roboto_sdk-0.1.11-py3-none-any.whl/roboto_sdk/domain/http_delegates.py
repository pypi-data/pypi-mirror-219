#  Copyright (c) 2023 Roboto Technologies, Inc.

import dataclasses

from ..http import HttpClient, PATAuthDecorator
from ..profile import RobotoProfile
from .actions import (
    ActionHttpDelegate,
    InvocationHttpDelegate,
)
from .datasets import DatasetHttpDelegate
from .orgs import OrgHttpDelegate
from .tokens import TokenHttpDelegate
from .triggers import TriggerHttpDelegate
from .users import UserHttpDelegate


@dataclasses.dataclass(frozen=True)
class HttpDelegates:
    actions: ActionHttpDelegate
    datasets: DatasetHttpDelegate
    invocations: InvocationHttpDelegate
    orgs: OrgHttpDelegate
    tokens: TokenHttpDelegate
    triggers: TriggerHttpDelegate
    users: UserHttpDelegate

    @staticmethod
    def from_profile(profile: RobotoProfile, entry_name: str = "default"):
        entry = profile.get_entry(entry_name)
        auth = PATAuthDecorator.for_client(
            client_id=entry.default_client_id, profile=profile
        )
        http = HttpClient(default_endpoint=entry.default_endpoint, default_auth=auth)

        # Take endpoint explicitly
        actions = ActionHttpDelegate(
            roboto_service_base_url=entry.default_endpoint, http_client=http
        )
        datasets = DatasetHttpDelegate(
            roboto_service_base_url=entry.default_endpoint, http_client=http
        )
        invocations = InvocationHttpDelegate(
            roboto_service_base_url=entry.default_endpoint, http_client=http
        )

        # Take endpoint implicitly through client
        orgs = OrgHttpDelegate(http_client=http)
        tokens = TokenHttpDelegate(http_client=http)
        triggers = TriggerHttpDelegate(http_client=http)
        users = UserHttpDelegate(http_client=http)

        return HttpDelegates(
            actions=actions,
            datasets=datasets,
            invocations=invocations,
            orgs=orgs,
            tokens=tokens,
            triggers=triggers,
            users=users,
        )
