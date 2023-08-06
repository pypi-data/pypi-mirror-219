import abc
import datetime
import enum
from typing import Any, Optional

import pydantic

from ...pagination import PaginatedList
from ...serde import pydantic_jsonable_dict
from ...time import utcnow
from ..files import FileRecord
from .record import (
    Administrator,
    DatasetRecord,
    StorageLocation,
)


class AccessMode(enum.Enum):
    ReadOnly = "ReadOnly"
    ReadWrite = "ReadWrite"


class Credentials(pydantic.BaseModel):
    access_key_id: str
    bucket: str
    expiration: datetime.datetime
    secret_access_key: str
    session_token: str
    required_prefix: str

    def is_expired(self) -> bool:
        return utcnow() >= self.expiration

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self)


class DatasetDelegate(abc.ABC):
    @abc.abstractmethod
    def create_dataset(
        self,
        administrator: Administrator = Administrator.Roboto,
        metadata: Optional[dict[str, Any]] = None,
        storage_location: StorageLocation = StorageLocation.S3,
        tags: Optional[list[str]] = None,
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> DatasetRecord:
        raise NotImplementedError("create_dataset")

    @abc.abstractmethod
    def get_dataset_by_primary_key(
        self,
        dataset_id: str,
        org_id: Optional[str] = None,
    ) -> DatasetRecord:
        raise NotImplementedError("get_dataset_by_primary_key")

    @abc.abstractmethod
    def get_temporary_credentials(
        self, record: DatasetRecord, mode: AccessMode, caller: Optional[str] = None
    ) -> Credentials:
        raise NotImplementedError("get_temporary_credentials")

    @abc.abstractmethod
    def list_files(
        self,
        dataset_id: str,
        org_id: Optional[str] = None,
        page_token: Optional[dict[str, str]] = None,
    ) -> PaginatedList[FileRecord]:
        raise NotImplementedError("list_files")

    @abc.abstractmethod
    def query_datasets(
        self,
        filters: dict[str, Any],
        org_id: Optional[str] = None,
        page_token: Optional[dict[str, str]] = None,
    ) -> PaginatedList[DatasetRecord]:
        raise NotImplementedError("query_datasets")
