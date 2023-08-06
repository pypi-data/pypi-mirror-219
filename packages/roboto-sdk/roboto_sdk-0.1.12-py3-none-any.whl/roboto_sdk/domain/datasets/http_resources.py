from typing import Any

import pydantic

from .record import Administrator, StorageLocation


class CreateDatasetRequest(pydantic.BaseModel):
    administrator: Administrator
    storage_location: StorageLocation
    metadata: dict[str, Any] = pydantic.Field(default_factory=dict)
    tags: list[str] = pydantic.Field(default_factory=list)
