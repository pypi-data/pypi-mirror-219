import datetime
import enum
from typing import Optional

import pydantic

from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)


class InvocationDataSourceType(enum.Enum):
    """Source of data for an Action's InputBinding"""

    Dataset = "Dataset"


class InvocationDataSource(pydantic.BaseModel):
    data_source_type: InvocationDataSourceType
    # The "type" determines the meaning of "id":
    #   - if type is "Dataset," id is a dataset_id
    data_source_id: str


class InvocationSource(enum.Enum):
    Trigger = "Trigger"
    Manual = "Manual"


class InvocationProvenance(pydantic.BaseModel):
    source_type: InvocationSource
    # The “type” determines the meaning of “id:”
    #   - if type is “Trigger,” id is a TriggerId;
    #   - if type is “Manual,” id is a UserId.
    source_id: str


class InvocationStatus(enum.Enum):
    Queued = "Queued"
    Scheduled = "Scheduled"
    Downloading = "Downloading"
    Processing = "Processing"
    Uploading = "Uploading"
    Completed = "Completed"
    Failed = "Failed"
    Deadly = "Deadly"

    def is_terminal(self) -> bool:
        return self in {
            InvocationStatus.Completed,
            InvocationStatus.Failed,
            InvocationStatus.Deadly,
        }


class InvocationStatusRecord(pydantic.BaseModel):
    status: InvocationStatus
    detail: Optional[str] = None
    timestamp: datetime.datetime  # Persisted as ISO 8601 string in UTC


class InvocationRecord(pydantic.BaseModel):
    action_name: str
    created: datetime.datetime  # Persisted as ISO 8601 string in UTC
    data_source: InvocationDataSource
    input_data: list[str]
    invocation_id: str  # Partition key
    logs_bucket: Optional[str] = None
    logs_prefix: Optional[str] = None
    compute_requirements: ComputeRequirements
    container_parameters: ContainerParameters
    org_id: str
    provenance: InvocationProvenance
    status: list[InvocationStatusRecord] = pydantic.Field(default_factory=list)


class LogRecord(pydantic.BaseModel):
    log: str
    timestamp: datetime.datetime
