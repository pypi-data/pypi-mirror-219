import pathlib
from typing import Optional

from ...exceptions import RobotoHttpExceptionParse
from ...http import HttpClient
from ...serde import pydantic_jsonable_dict
from .delegate import FileDelegate, FileTag
from .http_resources import (
    CreateFileRequest,
    DeleteFileRequest,
)
from .record import FileRecord


class FileHttpDelegate(FileDelegate):
    """
    A file delegate intended for service/admin-use only. Public methods are not implemented.
    Capable of making HTTP requests to the Roboto API to memorialize file records.
    """

    __http_client: HttpClient
    __roboto_service_base_url: str

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient) -> None:
        super().__init__()
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url

    def delete_file(self, key: str) -> None:
        raise NotImplementedError("delete_file")

    def download_file(self, key: str, local_path: pathlib.Path) -> None:
        raise NotImplementedError("download_file")

    def upload_file(
        self,
        local_path: pathlib.Path,
        key: str,
        tags: Optional[dict[FileTag, str]] = None,
    ) -> None:
        raise NotImplementedError("upload_file")

    def get_signed_url(self, key: str) -> str:
        raise NotImplementedError("get_signed_url")

    def protected_upsert_file_record(
        self,
        bucket: str,
        key: str,
    ) -> FileRecord:
        url = f"{self.__roboto_service_base_url}/v1/files"
        request = CreateFileRequest(
            bucket=bucket,
            key=key,
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.put(
                url,
                data=pydantic_jsonable_dict(request),
                headers={"Content-Type": "application/json"},
            )
        return FileRecord.parse_obj(response.from_json(json_path=["data"]))

    def protected_delete_file_record(
        self,
        bucket: str,
        key: str,
    ) -> None:
        url = f"{self.__roboto_service_base_url}/v1/files"
        request = DeleteFileRequest(
            bucket=bucket,
            key=key,
        )

        with RobotoHttpExceptionParse():
            self.__http_client.delete(
                url,
                data=pydantic_jsonable_dict(request),
                headers={"Content-Type": "application/json"},
            )
