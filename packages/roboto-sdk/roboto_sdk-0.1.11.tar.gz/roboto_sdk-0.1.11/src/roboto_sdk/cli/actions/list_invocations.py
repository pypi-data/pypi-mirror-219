#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json

from ...domain.actions import Invocation
from ..args import add_org_arg
from ..command import RobotoCommand
from ..context import CLIContext


def list_invocations(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    matching_invocations = Invocation.query(
        {"action_name": args.name},
        invocation_delegate=context.invocations,
        org_id=args.org,
    )
    print(
        json.dumps(
            [invocation.to_dict() for invocation in matching_invocations], indent=4
        )
    )


def list_invocations_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--name",
        required=False,
        action="store",
        help="If querying by action name, must provide an exact match; patterns are not accepted.",
    )
    add_org_arg(parser=parser)


list_invocations_command = RobotoCommand(
    name="list-invocations",
    logic=list_invocations,
    setup_parser=list_invocations_parser,
    command_kwargs={"help": "List invocations for action."},
)
