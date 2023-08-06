import abc
import enum
import pathlib
from typing import Optional

from .record import FileRecord


class FileTag(enum.Enum):
    DatasetId = "dataset_id"
    OrgId = "org_id"
    # Path to file relative to common prefix
    CommonPrefix = "common_prefix"


class FileDelegate(abc.ABC):
    @abc.abstractmethod
    def delete_file(self, key: str) -> None:
        raise NotImplementedError("delete_file")

    @abc.abstractmethod
    def download_file(self, key: str, local_path: pathlib.Path) -> None:
        raise NotImplementedError("download_file")

    @abc.abstractmethod
    def upload_file(
        self,
        local_path: pathlib.Path,
        key: str,
        tags: Optional[dict[FileTag, str]] = None,
    ) -> None:
        raise NotImplementedError("upload_file")

    @abc.abstractmethod
    def protected_upsert_file_record(
        self,
        bucket: str,
        key: str,
    ) -> FileRecord:
        raise NotImplementedError("protected_upsert_file_record")

    @abc.abstractmethod
    def protected_delete_file_record(
        self,
        bucket: str,
        key: str,
    ) -> None:
        raise NotImplementedError("protected_delete_file_record")
