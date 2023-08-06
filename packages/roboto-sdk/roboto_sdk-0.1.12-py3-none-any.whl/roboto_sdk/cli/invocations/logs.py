#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import time
from typing import Optional

from ...domain.actions import Invocation
from ...exceptions import RobotoNotFoundException
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def get_logs(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    invocation = Invocation.from_id(
        args.invocation_id,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )

    page_token: Optional[str] = None
    try:
        wait_msg = ""
        while True:
            try:
                log_record_generator = invocation.get_logs(page_token)
                while True:
                    log_record = next(log_record_generator)
                    if wait_msg:
                        print("\r", " " * len(wait_msg), end="\r", flush=True)
                        wait_msg = ""
                    print(log_record.log)
            except RobotoNotFoundException:
                if args.tail:
                    if invocation.reached_terminal_status:
                        break
                    if not wait_msg:
                        wait_msg = "Waiting for logs..."
                        print(wait_msg, end="", flush=True)
                    invocation.refresh()
                    time.sleep(2)
                else:
                    print("No logs found.")
                    break
            except StopIteration as stop:
                if args.tail and not invocation.reached_terminal_status:
                    time.sleep(2)
                    invocation.refresh()
                    page_token = stop.value
                else:
                    break
    except KeyboardInterrupt:
        return  # Swallow


def get_logs_parser(parser: argparse.ArgumentParser):
    parser.add_argument("invocation_id")
    parser.add_argument("--tail", required=False, action="store_true")
    add_org_arg(parser=parser)


get_logs_command = RobotoCommand(
    name="logs",
    logic=get_logs,
    setup_parser=get_logs_parser,
    command_kwargs={"help": "Get invocation logs."},
)
