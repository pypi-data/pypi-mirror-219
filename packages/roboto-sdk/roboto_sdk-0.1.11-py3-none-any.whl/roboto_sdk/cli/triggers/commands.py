#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse
import json
import sys

from ...domain.triggers import Trigger
from ..args import add_org_arg
from ..command import (
    RobotoCommand,
    RobotoCommandSet,
)
from ..context import CLIContext

NAME_PARAM_HELP = "The unique name used to reference a trigger."
ACTION_NAME_PARAM_HELP = (
    "The unique name used to reference an action which a certain trigger invokes."
)


def create(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Trigger.create(
        name=args.name,
        action_name=args.action_name,
        org_id=args.org,
        action_delegate=context.actions,
        trigger_delegate=context.triggers,
    )
    sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def create_setup_parser(parser):
    parser.add_argument("--name", type=str, required=True, help=NAME_PARAM_HELP)
    parser.add_argument(
        "--action-name", type=str, required=True, help=ACTION_NAME_PARAM_HELP
    )
    add_org_arg(parser=parser)


def get(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Trigger.from_name(
        name=args.name,
        org_id=args.org,
        action_delegate=context.actions,
        trigger_delegate=context.triggers,
    )
    sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def get_setup_parser(parser):
    parser.add_argument("--name", type=str, required=True, help=NAME_PARAM_HELP)
    add_org_arg(parser=parser)


def query(args, context: CLIContext, parser: argparse.ArgumentParser):
    records = Trigger.query(
        filters=None,
        org_id=args.org,
        action_delegate=context.actions,
        trigger_delegate=context.triggers,
    )
    for record in records:
        sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def query_setup_parser(parser):
    add_org_arg(parser=parser)


create_command = RobotoCommand(
    name="create",
    logic=create,
    setup_parser=create_setup_parser,
    command_kwargs={
        "help": "Creates a trigger to automatically invoke some action on datasets when certain criteria are met"
    },
)

get_command = RobotoCommand(
    name="get",
    logic=get,
    setup_parser=get_setup_parser,
    command_kwargs={"help": "Looks up a specific trigger by name"},
)

query_command = RobotoCommand(
    name="query",
    logic=query,
    setup_parser=query_setup_parser,
    command_kwargs={
        "help": "Queries many triggers that meet a certain condition. Constrained to a single org."
    },
)

commands = [create_command, get_command, query_command]

command_set = RobotoCommandSet(
    name="triggers",
    help="Commands for managing triggers which automatically invoke actions on datasets when certain criteria are met",
    commands=commands,
)
