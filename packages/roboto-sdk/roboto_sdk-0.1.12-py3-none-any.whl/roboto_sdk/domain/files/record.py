import datetime

import pydantic


class FileRecord(pydantic.BaseModel):
    association_id: str  # e.g. dataset_id, collection_id, etc. GSI PK.
    modified: datetime.datetime  # Persisted as ISO 8601 string in UTC
    relative_path: str  # path relative to some common prefix. Used as local path when downloaded.
    size: int  # bytes
    org_id: str
    uri: str  # Primary key
