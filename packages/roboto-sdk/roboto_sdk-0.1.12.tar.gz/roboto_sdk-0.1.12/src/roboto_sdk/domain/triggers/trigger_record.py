#  Copyright (c) 2023 Roboto Technologies, Inc.


from typing import Optional

import pydantic

from ..actions import (
    ComputeRequirements,
    ContainerParameters,
)


class TriggerRecord(pydantic.BaseModel):
    name: str  # Sort Key
    org_id: str  # Partition Key
    action_name: str
    required_inputs: list[str]
    additional_inputs: Optional[list[str]] = None
    compute_requirement_overrides: Optional[ComputeRequirements] = None
    container_parameter_overrides: Optional[ContainerParameters] = None
