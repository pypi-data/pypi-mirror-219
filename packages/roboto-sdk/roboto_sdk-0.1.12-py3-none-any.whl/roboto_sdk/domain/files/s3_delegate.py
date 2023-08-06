import pathlib
from typing import Any, Optional, Protocol
import urllib.parse

import boto3
import botocore.config

from .delegate import FileDelegate, FileTag
from .progress import (
    ProgressMonitor,
    ProgressMonitorFactory,
)
from .record import FileRecord


class S3Credentials(Protocol):
    access_key_id: str
    secret_access_key: str
    session_token: str


class FileS3Delegate(FileDelegate):
    """
    A file delegate intented for client-side use. Protected methods are not implemented.
    Capable of uploading and deleting files from S3 given an authenticated boto3 Bucket resource.
    """

    __s3_bucket: str
    __s3_client: Any  # boto3.client("s3")
    __progress_monitor_factory: Optional[ProgressMonitorFactory]

    def __init__(
        self,
        bucket_name: Any,
        credentials: S3Credentials,
        s3_client: Optional[Any] = None,
        progress_monitor_factory: Optional[ProgressMonitorFactory] = None,
    ) -> None:
        self.__s3_client = (
            s3_client
            if s3_client is not None
            else FileS3Delegate.generate_s3_client(credentials=credentials)
        )
        self.__s3_bucket = bucket_name
        self.__progress_monitor_factory = progress_monitor_factory

    def delete_file(self, key: str) -> None:
        self.__s3_client.delete_objects(
            Bucket=self.__s3_bucket,
            Delete={
                "Objects": [{"Key": key}],
            },
        )

    def download_file(self, key: str, local_path: pathlib.Path) -> None:
        local_path.parent.mkdir(parents=True, exist_ok=True)

        if self.__progress_monitor_factory is not None:
            res = self.__s3_client.head_object(Bucket=self.__s3_bucket, Key=key)
            download_bytes = int(res.get("ContentLength", 0))

            progress_monitor = self.__progress_monitor_factory.download_monitor(
                source=key, size=download_bytes
            )
            try:
                self.__s3_client.download_file(
                    Bucket=self.__s3_bucket,
                    Key=key,
                    Filename=str(local_path),
                    Callback=progress_monitor.update,
                )
            finally:
                progress_monitor.close()
        else:
            self.__s3_client.download_file(
                Bucket=self.__s3_bucket,
                Key=key,
                Filename=str(local_path),
            )

    def upload_file(
        self,
        local_path: pathlib.Path,
        key: str,
        tags: Optional[dict[FileTag, str]] = None,
    ) -> None:
        upload_file_args: dict[str, Any] = {
            "Filename": str(local_path),
            "Key": key,
            "Bucket": self.__s3_bucket,
        }

        if tags is not None:
            serializable_tags = {tag.value: value for tag, value in tags.items()}
            encoded_tags = urllib.parse.urlencode(serializable_tags)
            upload_file_args["ExtraArgs"] = {"Tagging": encoded_tags}

        progress_monitor: Optional[ProgressMonitor]
        if self.__progress_monitor_factory is not None:
            progress_monitor = self.__progress_monitor_factory.download_monitor(
                source=key, size=local_path.stat().st_size
            )
            upload_file_args["Callback"] = progress_monitor.update

        try:
            self.__s3_client.upload_file(**upload_file_args)
        finally:
            if progress_monitor is not None:
                progress_monitor.close()

    def get_signed_url(self, key: str) -> str:
        return self.__s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.__s3_bucket, "Key": key},
            ExpiresIn=(60 * 60),
        )

    def protected_upsert_file_record(
        self,
        bucket: str,
        key: str,
    ) -> FileRecord:
        """Admin only"""
        raise NotImplementedError("protected_upsert_file_record")

    def protected_delete_file_record(
        self,
        bucket: str,
        key: str,
    ) -> None:
        """Admin only"""
        raise NotImplementedError("protected_delete_file_record")

    @staticmethod
    def generate_s3_client(credentials: S3Credentials, tcp_keepalive: bool = False):
        session = boto3.Session(
            aws_access_key_id=credentials.access_key_id,
            aws_secret_access_key=credentials.secret_access_key,
            aws_session_token=credentials.session_token,
        )

        return session.client(
            "s3", config=botocore.config.Config(tcp_keepalive=tcp_keepalive)
        )
