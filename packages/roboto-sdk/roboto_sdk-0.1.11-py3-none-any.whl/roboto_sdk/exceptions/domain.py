#  Copyright (c) 2023 Roboto Technologies, Inc.

import json
import re
from typing import Optional

from ..http import HttpError

__ORG_MESSAGE_PATTERN = re.compile(r"did not provide a org for single-org operation.")


class RobotoDomainException(Exception):
    """
    Expected exceptions from the Roboto domain entity objects.
    """

    @staticmethod
    def from_client_error(error: HttpError):
        message: Optional[str]

        if type(error.msg) is dict:
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


class RobotoHttpExceptionParse(object):
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception, traceback):
        if issubclass(type(exception), HttpError):
            raise RobotoDomainException.from_client_error(error=exception)


class RobotoUnauthorizedException(RobotoDomainException):
    """
    Thrown when a user is attempting to access a resource that they do not have permission to access
    """


class RobotoNotFoundException(RobotoDomainException):
    """
    Throw when a requested resource does not exist
    """


class RobotoInvalidRequestException(RobotoDomainException):
    """
    Thrown when request parameters are in some way invalid
    """


class RobotoNoOrgProvidedException(RobotoDomainException):
    """
    Thrown when no org is provided to an operation which requires an org.
    """


class RobotoServiceError(RobotoDomainException):
    """
    Thrown when Roboto Service failed in an unexpected way
    """
