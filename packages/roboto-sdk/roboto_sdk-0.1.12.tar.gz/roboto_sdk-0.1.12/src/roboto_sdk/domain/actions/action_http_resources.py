from typing import Any, Optional

import pydantic

from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)
from .action_delegate import UpdateCondition


class CreateActionRequest(pydantic.BaseModel):
    # Required
    name: str

    # Optional
    description: Optional[str] = None
    metadata: Optional[dict[str, Any]] = pydantic.Field(default_factory=dict)
    tags: Optional[list[str]] = pydantic.Field(default_factory=list)
    compute_requirements: Optional[ComputeRequirements] = None
    container_parameters: Optional[ContainerParameters] = None


class ContainerUploadCredentials(pydantic.BaseModel):
    username: str
    password: str
    registry_url: str
    image_uri: str


class UpdateActionRequest(pydantic.BaseModel):
    updates: dict[str, Any]
    conditions: Optional[list[UpdateCondition]] = None
