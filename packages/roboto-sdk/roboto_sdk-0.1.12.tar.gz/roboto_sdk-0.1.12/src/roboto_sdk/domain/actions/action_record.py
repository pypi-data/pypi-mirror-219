import datetime
from typing import Any, Optional

import pydantic

from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)


class ActionRecord(pydantic.BaseModel):
    """
    Actions are unique by their org_id and name.

    Note: update Action.DISALLOWED_FOR_UPDATE if necessary when adding/updating/removing fields.
    """

    created: datetime.datetime  # Persisted as ISO 8601 string in UTC
    created_by: str
    modified: datetime.datetime  # Persisted as ISO 8601 string in UTC
    modified_by: str
    name: str  # Sort key
    org_id: str  # Partition key

    compute_requirements: ComputeRequirements = pydantic.Field(
        default_factory=ComputeRequirements
    )
    container_parameters: ContainerParameters = pydantic.Field(
        default_factory=ContainerParameters
    )
    description: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None
    tags: Optional[list[str]] = None
    uri: Optional[str] = None
