#  Copyright (c) 2023 Roboto Technologies, Inc.
import enum
import json
import os
import pathlib
from typing import Any, Optional

import pydantic

from ..logging import default_logger

log = default_logger()

PROFILE_ENV_VAR = "ROBOTO_PROFILE"

PROD_USER_POOL_CLIENT_ID = "1gricmdmh0vv582qdd84phab5"
PROD_ENDPOINT = "https://api.roboto.ai"

DEFAULT_ROBOTO_CONFIG_DIR = pathlib.Path(f"{pathlib.Path.home()}/.roboto")
DEFAULT_ROBOTO_PROFILE_FILE = pathlib.Path(f"{DEFAULT_ROBOTO_CONFIG_DIR}/config.json")


class RobotoProfileEntry(pydantic.BaseModel):
    user_id: str
    token: str
    default_endpoint: str = PROD_ENDPOINT
    default_client_id: str = PROD_USER_POOL_CLIENT_ID


class RobotoProfileFileType(str, enum.Enum):
    none = "none"
    malformed = "malformed"
    implicit = "implicit"
    explicit = "explicit"


class RobotoProfile:
    __config_file: pathlib.Path

    def __init__(self, config_file: pathlib.Path = DEFAULT_ROBOTO_PROFILE_FILE):
        self.__config_file = config_file

    def __base_entry_from_file(
        self,
        profile_name: Optional[str],
    ) -> tuple[RobotoProfileFileType, Optional[RobotoProfileEntry]]:
        if not self.__config_file.is_file():
            return RobotoProfileFileType.none, None

        with open(self.__config_file, "r") as f:
            contents: dict[str, Any] = json.loads(f.read())

        profile_to_check = "default" if profile_name is None else profile_name
        if profile_to_check in contents.keys():
            try:
                return RobotoProfileFileType.explicit, RobotoProfileEntry.parse_obj(
                    contents.get(profile_to_check)
                )
            except pydantic.ValidationError:
                log.warning(
                    f"Couldn't parse {self.__config_file} as a multi-profile 'explicit' type"
                )
                return RobotoProfileFileType.malformed, None

        try:
            return RobotoProfileFileType.implicit, RobotoProfileEntry.parse_obj(
                contents
            )
        except pydantic.ValidationError:
            log.warning(
                f"Couldn't parse {self.__config_file} as single-profile 'implicit' type"
            )
            return RobotoProfileFileType.malformed, None

    def get_entry(self, profile_name: Optional[str] = None) -> RobotoProfileEntry:
        profile_to_check = (
            profile_name
            if profile_name is not None
            else os.getenv(PROFILE_ENV_VAR, "default")
        )
        # TODO - Support AWS style order of precedence
        file_type, entry = self.__base_entry_from_file(profile_to_check)

        if file_type == RobotoProfileFileType.malformed:
            raise ValueError(f"Malformed roboto profile file '{self.__config_file}'")
        elif file_type == RobotoProfileFileType.none:
            raise ValueError(f"Missing roboto profile file '{self.__config_file}'")

        assert entry is not None
        return entry
