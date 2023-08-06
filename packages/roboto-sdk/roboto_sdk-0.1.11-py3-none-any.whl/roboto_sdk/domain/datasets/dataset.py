import collections.abc
import pathlib
from typing import Any, Optional

import pathspec

from ...serde import pydantic_jsonable_dict
from ..files import (
    File,
    FileDelegate,
    FileS3Delegate,
    FileTag,
)
from ..files.progress import (
    TqdmProgressMonitorFactory,
)
from .delegate import (
    AccessMode,
    Credentials,
    DatasetDelegate,
    StorageLocation,
)
from .record import Administrator, DatasetRecord


class Dataset:
    __delegate: DatasetDelegate
    __record: DatasetRecord
    __files_delegate: Optional[FileDelegate] = None
    __temp_credentials: Optional[Credentials] = None

    @classmethod
    def create(
        cls,
        dataset_delegate: DatasetDelegate,
        administrator: Administrator = Administrator.Roboto,
        storage_location: StorageLocation = StorageLocation.S3,
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        tags: Optional[list[str]] = None,
        files_delegate: Optional[FileDelegate] = None,
    ) -> "Dataset":
        record = dataset_delegate.create_dataset(
            administrator, metadata, storage_location, tags, org_id, created_by
        )
        return cls(record, dataset_delegate, files_delegate)

    @classmethod
    def from_id(
        cls,
        dataset_id: str,
        dataset_delegate: DatasetDelegate,
        org_id: Optional[str] = None,
        files_delegate: Optional[FileDelegate] = None,
    ) -> "Dataset":
        record = dataset_delegate.get_dataset_by_primary_key(dataset_id, org_id)
        return cls(record, dataset_delegate, files_delegate)

    @classmethod
    def query(
        cls,
        filters: dict[str, Any],
        dataset_delegate: DatasetDelegate,
        files_delegate: Optional[FileDelegate] = None,
        org_id: Optional[str] = None,
    ) -> collections.abc.Generator["Dataset", None, None]:
        known_keys = set(DatasetRecord.__fields__.keys())
        actual_keys = set(filters.keys())
        unknown_keys = actual_keys - known_keys
        if unknown_keys:
            plural = len(unknown_keys) > 1
            msg = (
                "are not known attributes of Dataset"
                if plural
                else "is not a known attribute of Dataset"
            )
            raise ValueError(f"{unknown_keys} {msg}. Known attributes: {known_keys}")

        paginated_results = dataset_delegate.query_datasets(filters, org_id=org_id)
        while True:
            for record in paginated_results.items:
                yield cls(record, dataset_delegate, files_delegate)
            if paginated_results.next_token:
                paginated_results = dataset_delegate.query_datasets(
                    filters, org_id=org_id, page_token=paginated_results.next_token
                )
            else:
                break

    def __init__(
        self,
        record: DatasetRecord,
        delegate: DatasetDelegate,
        files_delegate: Optional[FileDelegate] = None,
    ) -> None:
        self.__delegate = delegate
        self.__files_delegate = files_delegate
        self.__record = record

    @property
    def dataset_id(self) -> str:
        return self.__record.dataset_id

    def download_files(
        self,
        out_path: pathlib.Path,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
    ) -> None:
        """
        Download files associated with this dataset to the given directory.
        If `out_path` does not exist, it will be created.

        `include_patterns` and `exclude_patterns` are lists of gitignore-style patterns.
        See https://git-scm.com/docs/gitignore.

        Example:
        ```
        dataset = datasets.Dataset.by_id("<dataset_id>", dataset_delegate)
        dataset.download_files(
            pathlib.Path("/tmp/tmp.nV1gdW5WHV"),
            include_patterns=["**/*.g4"],
            exclude_patterns=["**/test/**"]
        )
        ```
        """
        if (
            self.__record.storage_location != StorageLocation.S3
            or self.__record.administrator != Administrator.Roboto
        ):
            raise NotImplementedError(
                "Only S3-backed storage administered by Roboto is supported at this time."
            )

        if not out_path.is_dir():
            out_path.mkdir(parents=True)

        credentials = self.get_temporary_credentials(AccessMode.ReadOnly)

        files_delegate = (
            self.__files_delegate
            if self.__files_delegate is not None
            else FileS3Delegate(
                bucket_name=credentials.bucket,
                credentials=credentials,
                s3_client=FileS3Delegate.generate_s3_client(
                    credentials=credentials, tcp_keepalive=True
                ),
                progress_monitor_factory=TqdmProgressMonitorFactory(concurrency=1),
            )
        )
        for file in self.list_files(include_patterns, exclude_patterns):
            local_path = out_path / file.relative_path
            files_delegate.download_file(file.key, local_path)

    def get_temporary_credentials(
        self,
        mode: AccessMode = AccessMode.ReadOnly,
        caller: Optional[str] = None,  # A Roboto user_id
    ) -> Credentials:
        if self.__temp_credentials is None or self.__temp_credentials.is_expired():
            self.__temp_credentials = self.__delegate.get_temporary_credentials(
                self.__record, mode, caller
            )
        return self.__temp_credentials

    def list_files(
        self,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
    ) -> collections.abc.Generator[File, None, None]:
        """
        `include_patterns` and `exclude_patterns` are lists of gitignore-style patterns.
        See https://git-scm.com/docs/gitignore.
        """
        include_pattern_spec: Optional[pathspec.PathSpec] = None
        if include_patterns is not None:
            include_pattern_spec = pathspec.PathSpec.from_lines(
                pathspec.patterns.GitWildMatchPattern, include_patterns
            )

        exclude_pattern_spec: Optional[pathspec.PathSpec] = None
        if exclude_patterns is not None:
            exclude_pattern_spec = pathspec.GitIgnoreSpec.from_lines(exclude_patterns)

        paginated_results = self.__delegate.list_files(
            self.__record.dataset_id, self.__record.org_id
        )
        while True:
            for record in paginated_results.items:
                file = File(record)
                if include_pattern_spec and not include_pattern_spec.match_file(
                    file.relative_path
                ):
                    """Given file does not match any of the include patterns."""
                    continue
                if exclude_pattern_spec and exclude_pattern_spec.match_file(
                    file.relative_path
                ):
                    """Given file matches one of the exclude patterns."""
                    continue
                yield file
            if paginated_results.next_token:
                paginated_results = self.__delegate.list_files(
                    self.__record.dataset_id,
                    self.__record.org_id,
                    paginated_results.next_token,
                )
            else:
                break

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    def upload_directory(
        self,
        directory_path: pathlib.Path,
        exclude_patterns: Optional[list[str]] = None,
    ) -> None:
        """
        Upload everything, recursively, in directory, ignoring files that match any of the ignore patterns.

        `exclude_patterns` is a list of gitignore-style patterns.
        See https://git-scm.com/docs/gitignore#_pattern_format.

        Example:
        ```
        dataset.upload_directory(
            pathlib.Path("/path/to/directory"),
            exclude_patterns=[
                "__pycache__/",
                "*.pyc",
                "node_modules/",
                "**/*.log",
            ],
        )
        ```
        """
        if not directory_path.is_dir():
            raise ValueError(f"{directory_path} is not a directory")

        exclude_spec: Optional[pathspec.PathSpec] = None
        if exclude_patterns is not None:
            exclude_spec = pathspec.GitIgnoreSpec.from_lines(
                exclude_patterns,
            )

        def _upload_directory(directory_path: pathlib.Path, key_prefix: str) -> None:
            for path in directory_path.iterdir():
                if path.is_dir():
                    _upload_directory(path, f"{key_prefix}/{path.name}")
                else:
                    if exclude_spec is not None and exclude_spec.match_file(path):
                        continue
                    self.upload_file(path, f"{key_prefix}/{path.name}")

        _upload_directory(directory_path, "")

    def upload_file(
        self,
        local_file_path: pathlib.Path,
        key: str,
    ) -> None:
        """
        Uploads a file to the dataset's storage location.

        :param file_path: The path to the file to upload.
        :param key: The key to use for the file in the dataset's storage location.
                    It will be prefixed with the dataset's storage prefix.
        """
        if not local_file_path.is_file():
            raise ValueError(f"{local_file_path} is not a file")

        if (
            self.__record.storage_location != StorageLocation.S3
            or self.__record.administrator != Administrator.Roboto
        ):
            raise NotImplementedError(
                "Only S3-backed storage administered by Roboto is supported at this time."
            )

        credentials = self.get_temporary_credentials(AccessMode.ReadWrite)
        files_delegate = (
            self.__files_delegate
            if self.__files_delegate is not None
            else FileS3Delegate(
                bucket_name=credentials.bucket,
                credentials=credentials,
                s3_client=FileS3Delegate.generate_s3_client(
                    credentials=credentials, tcp_keepalive=True
                ),
                progress_monitor_factory=TqdmProgressMonitorFactory(concurrency=1),
            )
        )
        key = f"{credentials.required_prefix}/{key.lstrip('/')}"
        files_delegate.upload_file(
            local_file_path,
            key,
            tags={
                FileTag.DatasetId: self.__record.dataset_id,
                FileTag.OrgId: self.__record.org_id,
                FileTag.CommonPrefix: credentials.required_prefix,
            },
        )
