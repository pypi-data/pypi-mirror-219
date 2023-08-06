#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Any

import pydantic

from .record import OrgRoleName, OrgType


class CreateOrgRequest(pydantic.BaseModel):
    org_type: OrgType
    name: str
    bind_email_domain: bool = False


class UpdateOrgRequest(pydantic.BaseModel):
    updates: dict[str, Any]


class BindEmailDomainRequest(pydantic.BaseModel):
    email_domain: str


class InviteUserRequest(pydantic.BaseModel):
    invited_user_id: str


class ModifyRoleForUserRequest(pydantic.BaseModel):
    user_id: str
    role_name: OrgRoleName


class RemoveUserFromOrgRequest(pydantic.BaseModel):
    user_id: str
