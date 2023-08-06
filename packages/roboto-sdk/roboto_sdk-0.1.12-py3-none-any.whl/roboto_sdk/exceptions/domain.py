#  Copyright (c) 2023 Roboto Technologies, Inc.

import json
import re
from typing import Any, Optional

from ..http import HttpError
from ..serde import safe_dict_drill

__ORG_MESSAGE_PATTERN = re.compile(r"did not provide a org for single-org operation.")


class RobotoDomainException(Exception):
    _message: str

    """
    Expected exceptions from the Roboto domain entity objects.
    """

    def __init__(self, message: str, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self._message = message

    @staticmethod
    def from_json(contents: dict[str, Any]) -> "RobotoDomainException":
        error_code = safe_dict_drill(contents, ["error", "error_code"])
        inner_message = safe_dict_drill(contents, ["error", "message"])

        if error_code is None or inner_message is None:
            raise ValueError("Need 'error_code' and 'message' available.")

        for subclass in RobotoDomainException.__subclasses__():
            if subclass.__name__ == error_code:
                return subclass(message=inner_message)

        raise ValueError("Unrecognized error code 'error_code'")

    @staticmethod
    def from_client_error(error: HttpError) -> "RobotoDomainException":
        message: Optional[str]

        if type(error.msg) is dict:
            # See if it's a first class RobotoException
            try:
                return RobotoDomainException.from_json(error.msg)
            except ValueError:
                pass

            # Handle JSON from non-roboto calls
            message = error.msg.get("message", json.dumps(error.msg))
        elif type(error.msg) is str:
            message = error.msg
        else:
            message = None

        if error.status is None:
            raise RobotoDomainException(error.msg)
        if error.status == 400:
            if (
                message is not None
                and "did not provide a org for single-org operation" in message
            ):
                return RobotoNoOrgProvidedException(error.msg)
            else:
                return RobotoInvalidRequestException(error.msg)
        if error.status in (401, 403):
            return RobotoUnauthorizedException(error.msg)
        if error.status == 404:
            return RobotoNotFoundException(error.msg)
        if 500 <= error.status < 600:
            return RobotoServiceError(error.msg)
        raise error

    @property
    def http_status_code(self) -> int:
        return 500

    @property
    def error_code(self) -> str:
        return self.__class__.__name__

    @property
    def message(self) -> str:
        return self._message

    def to_dict(self) -> dict[str, Any]:
        return {"error": {"error_code": self.error_code, "message": self.message}}

    def serialize(self) -> str:
        return json.dumps(self.to_dict())


class RobotoUnauthorizedException(RobotoDomainException):
    """
    Thrown when a user is attempting to access a resource that they do not have permission to access
    """

    @property
    def http_status_code(self) -> int:
        return 401


class RobotoNotFoundException(RobotoDomainException):
    """
    Throw when a requested resource does not exist
    """

    @property
    def http_status_code(self) -> int:
        return 404


class RobotoInvalidRequestException(RobotoDomainException):
    """
    Thrown when request parameters are in some way invalid
    """

    @property
    def http_status_code(self) -> int:
        return 400


class RobotoNoOrgProvidedException(RobotoDomainException):
    """
    Thrown when no org is provided to an operation which requires an org.
    """

    @property
    def http_status_code(self) -> int:
        return 400


class RobotoServiceError(RobotoDomainException):
    """
    Thrown when Roboto Service failed in an unexpected way
    """


class RobotoHttpExceptionParse(object):
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception, traceback):
        if issubclass(type(exception), HttpError):
            raise RobotoDomainException.from_client_error(error=exception)
