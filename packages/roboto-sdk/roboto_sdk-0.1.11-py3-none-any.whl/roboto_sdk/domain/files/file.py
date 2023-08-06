from typing import Optional
import urllib.parse

from .record import FileRecord


class File:
    __record: FileRecord
    __parsed_uri: Optional[urllib.parse.ParseResult] = None

    def __init__(self, record: FileRecord):
        self.__record = record

    @property
    def uri(self) -> str:
        return self.__record.uri

    @property
    def bucket(self) -> str:
        if self.__parsed_uri is None:
            self.__parsed_uri = urllib.parse.urlparse(self.uri)
        return self.__parsed_uri.netloc

    @property
    def key(self) -> str:
        if self.__parsed_uri is None:
            self.__parsed_uri = urllib.parse.urlparse(self.uri)
        return self.__parsed_uri.path.lstrip("/")

    @property
    def relative_path(self) -> str:
        return self.__record.relative_path
