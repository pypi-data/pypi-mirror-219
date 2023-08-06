#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json

from ...domain.actions import Invocation
from ..args import add_org_arg
from ..command import RobotoCommand
from ..context import CLIContext


def show(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    invocation = Invocation.from_id(
        args.invocation_id,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )
    print(json.dumps(invocation.to_dict(), indent=4))
    return


def show_parser(parser: argparse.ArgumentParser):
    parser.add_argument("invocation_id")
    add_org_arg(parser=parser)


show_command = RobotoCommand(
    name="show",
    logic=show,
    setup_parser=show_parser,
    command_kwargs={"help": "Show invocation details."},
)
