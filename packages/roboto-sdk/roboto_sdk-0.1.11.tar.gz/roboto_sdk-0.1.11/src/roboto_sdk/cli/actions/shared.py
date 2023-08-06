#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import shlex
import textwrap
import typing

import pydantic

from ...domain.actions import (
    Action,
    ComputeRequirements,
    ContainerParameters,
)
from ..command import KeyValuePairsAction


def finalize_docker_image_registration_instructions(action: Action) -> str:
    # fmt: off
    return textwrap.dedent(f"""\
        If needed, finish registering Docker image with this action by pushing the image to Roboto's private registry:

            1. Tag your locally-built Docker image:
            $ docker tag <existing_image>:<existing_image_tag> {action.uri}

            2. Temporarily login to Roboto's private registry (requires Docker CLI; valid for 12hr):
            $ roboto actions docker-login --name '{action.name}'

            3. Push the Docker image
            $ docker push {action.uri}
    """)
    # fmt: on


class ParseError(Exception):
    msg: typing.Any

    def __init__(self, msg, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg


def parse_compute_requirements(
    args: argparse.Namespace,
    default_vcpu: typing.Optional[int] = None,
    default_memory: typing.Optional[int] = None,
    default_storage: typing.Optional[int] = None,
) -> typing.Optional[ComputeRequirements]:
    try:
        kwargs = {
            key: value
            for key, value in [
                ("vCPU", args.vcpu if args.vcpu else default_vcpu),
                ("memory", args.memory if args.memory else default_memory),
                ("storage", args.storage if args.storage else default_storage),
            ]
            if value is not None
        }
        if not kwargs:
            return None
        return ComputeRequirements.parse_obj(kwargs)
    except pydantic.ValidationError as exc:
        for err in exc.errors():
            err_msg = err.get("msg")
            msg = err_msg if err_msg else err
            raise ParseError(msg) from None

    return None


def decorate_parser_with_compute_requirements(parser: argparse.ArgumentParser) -> None:
    resource_requirements_group = parser.add_argument_group(
        "Resource requirements",
        "Specify required compute resources.",
    )
    resource_requirements_group.add_argument(
        "--vcpu",
        required=False,
        type=int,
        choices=[256, 512, 1024, 2048, 4096, 8192, 16384],
        help="CPU units to dedicate to this invocation. Defaults to 512 (0.5vCPU).",
    )

    resource_requirements_group.add_argument(
        "--memory",
        required=False,
        type=int,
        help=(
            "Memory (in MiB) to dedicate to this invocation. Defaults to 1024 (1 GiB). "
            "Supported values range from 512 (0.5 GiB) to 122880 (120 GiB), in increments of 1024 (1 GiB). "
            "Supported values are tied to selected vCPU resources. See documentation for more information."
        ),
    )

    resource_requirements_group.add_argument(
        "--storage",
        required=False,
        type=int,
        help=(
            "Ephemeral storage (in GiB) to dedicate to this invocation. Defaults to 21 GiB. "
            "Supported values range from 21 to 200, inclusive."
        ),
    )

    # Placeholder
    resource_requirements_group.add_argument(
        "--gpu",
        required=False,
        default=False,
        action="store_true",
        help=(
            "This is a placeholder; it currently does nothing. "
            "In the future, setting this option will invoke the action in a GPU-enabled compute environment."
        ),
    )


def parse_container_overrides(
    args: argparse.Namespace,
    default_entry_point: typing.Optional[list[str]] = None,
    default_command: typing.Optional[list[str]] = None,
    default_env_vars: typing.Optional[dict[str, str]] = None,
    default_workdir: typing.Optional[str] = None,
) -> typing.Optional[ContainerParameters]:
    try:
        kwargs = {
            key: value
            for key, value in [
                (
                    "entry_point",
                    args.entry_point if args.entry_point else default_entry_point,
                ),
                ("command", args.command if args.command else default_command),
                ("workdir", args.workdir if args.workdir else default_workdir),
                ("env_vars", args.env if args.env else default_env_vars),
            ]
            if value is not None
        }
        if not kwargs:
            return None
        return ContainerParameters.parse_obj(kwargs)
    except pydantic.ValidationError as exc:
        for err in exc.errors():
            err_msg = err.get("msg")
            msg = err_msg if err_msg else err
            raise ParseError(msg) from None

    return None


def decorate_parser_with_container_parameters(parser: argparse.ArgumentParser) -> None:
    group = parser.add_argument_group(
        "Container parameters",
        "Specify parameters to pass to the action's Docker container at runtime.",
    )

    group.add_argument(
        "--entrypoint",
        required=False,
        type=lambda entry_point: shlex.split(entry_point),
        dest="entry_point",
        help=(
            "Container ENTRYPOINT specified as a string. See documentation: "
            "https://docs.docker.com/engine/reference/run/#entrypoint-default-command-to-execute-at-runtime"
        ),
    )

    group.add_argument(
        "--command",
        required=False,
        type=lambda cmd: shlex.split(cmd),
        dest="command",
        help=(
            "Container CMD specified as a string. See documentation: "
            "https://docs.docker.com/engine/reference/run/#cmd-default-command-or-options"
        ),
    )

    group.add_argument(
        "--workdir",
        required=False,
        type=str,
        dest="workdir",
        help="See documentation: https://docs.docker.com/engine/reference/run/#workdir",
    )

    group.add_argument(
        "--env",
        required=False,
        metavar="KEY=VALUE",
        nargs="*",
        action=KeyValuePairsAction,
        help=(
            "Zero or more 'key=value' formatted pairs to set as container ENV vars. "
            "Do not use ENV vars for secrets (such as API keys). "
            "See documentation: https://docs.docker.com/engine/reference/run/#env-environment-variables"
        ),
    )
