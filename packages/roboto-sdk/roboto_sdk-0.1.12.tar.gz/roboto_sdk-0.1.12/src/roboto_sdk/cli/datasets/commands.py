#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json
import pathlib
import sys

from ...domain.datasets import Dataset
from ..command import (
    ExistingPathlibPath,
    KeyValuePairsAction,
    RobotoCommand,
    RobotoCommandSet,
)
from ..common_args import add_org_arg
from ..context import CLIContext

DATASET_ARG_HELP = "A unique ID used to reference a single dataset"


def create(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Dataset.create(
        dataset_delegate=context.datasets,
        metadata=args.metadata,
        tags=args.tag,
        org_id=args.org,
    )

    sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def create_setup_parser(parser):
    parser.add_argument(
        "-m",
        "--metadata",
        metavar="KEY=VALUE",
        nargs="*",
        action=KeyValuePairsAction,
        help="Zero or more 'key=value' format key/value pairs which represent dataset metadata. "
        + "Metadata can be mutated after creation.",
    )
    parser.add_argument(
        "-t",
        "--tag",
        type=str,
        nargs="*",
        help="One or more tags to annotate this dataset. Tags can be modified after creation.",
        action="extend",
    )
    add_org_arg(parser=parser)


def get(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Dataset.from_id(
        dataset_delegate=context.datasets, dataset_id=args.dataset_id, org_id=args.org
    )
    sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def get_setup_parser(parser):
    parser.add_argument(
        "-d", "--dataset-id", type=str, required=True, help=DATASET_ARG_HELP
    )
    add_org_arg(parser)


def query(args, context: CLIContext, parser: argparse.ArgumentParser):
    records = Dataset.query(
        filters=args.filter, dataset_delegate=context.datasets, org_id=args.org
    )
    for record in records:
        sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def query_setup_parser(parser):
    add_org_arg(parser=parser)
    parser.add_argument(
        "-f",
        "--filter",
        metavar="KEY=VALUE",
        nargs="*",
        action=KeyValuePairsAction,
        help="Zero or more 'key=value' formatted conditions which will perform equality checks against "
        + "datasets and filter results accordingly.",
        default={},
    )


def list_files(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Dataset.from_id(
        dataset_delegate=context.datasets, dataset_id=args.dataset_id, org_id=args.org
    )

    for f in record.list_files():
        sys.stdout.write(f"{f.relative_path}\n")


def list_files_setup_parser(parser):
    parser.add_argument(
        "-d", "--dataset-id", type=str, required=True, help=DATASET_ARG_HELP
    )
    add_org_arg(parser)


def upload_files(args, context: CLIContext, parser: argparse.ArgumentParser):
    path: pathlib.Path = args.path
    if args.exclude is not None and not path.is_dir():
        parser.error(
            "Exclude filters are only supported for directory uploads, not single files."
        )
    if args.key is not None and path.is_dir():
        parser.error(
            "Key overrides are only supported for single file uploads, now directories."
        )

    record = Dataset.from_id(
        dataset_delegate=context.datasets, dataset_id=args.dataset_id, org_id=args.org
    )

    if path.is_dir():
        record.upload_directory(directory_path=path, exclude_patterns=args.exclude)
    else:
        key = path.name if args.key is None else args.key
        record.upload_file(local_file_path=path, key=key)


def upload_files_setup_parser(parser):
    parser.add_argument(
        "-d", "--dataset-id", type=str, required=True, help=DATASET_ARG_HELP
    )
    parser.add_argument(
        "-k",
        "--key",
        type=str,
        help="A key to alias a file to when storing it to a dataset. Does nothing for directories.",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=ExistingPathlibPath,
        required=True,
        help="The path to a file or directory to upload.",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        type=str,
        nargs="*",
        help="Zero or more exclude filters (if path points to a directory)",
    )
    add_org_arg(parser)


def download_files(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Dataset.from_id(
        dataset_delegate=context.datasets, dataset_id=args.dataset_id, org_id=args.org
    )

    record.download_files(
        out_path=args.path, include_patterns=args.include, exclude_patterns=args.exclude
    )


def download_files_setup_parser(parser):
    parser.add_argument(
        "-d", "--dataset-id", type=str, required=True, help=DATASET_ARG_HELP
    )
    parser.add_argument(
        "-p",
        "--path",
        type=pathlib.Path,
        required=True,
        help="The download destination for this operation.",
    )
    parser.add_argument(
        "-i",
        "--include",
        type=str,
        nargs="*",
        help="Zero or more include filters (if path points to a directory)",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        type=str,
        nargs="*",
        help="Zero or more exclude filters (if path points to a directory)",
    )
    add_org_arg(parser)


create_command = RobotoCommand(
    name="create",
    logic=create,
    setup_parser=create_setup_parser,
    command_kwargs={"help": "Creates a new dataset."},
)

get_command = RobotoCommand(
    name="show",
    logic=get,
    setup_parser=get_setup_parser,
    command_kwargs={"help": "Gets information about a specific dataset."},
)

query_command = RobotoCommand(
    name="query",
    logic=query,
    setup_parser=query_setup_parser,
    command_kwargs={"help": "Queries for datasets which match search criteria."},
)

list_files_command = RobotoCommand(
    name="list-files",
    logic=list_files,
    setup_parser=list_files_setup_parser,
    command_kwargs={"help": "Lists files for a specific dataset."},
)

upload_files_command = RobotoCommand(
    name="upload-files",
    logic=upload_files,
    setup_parser=upload_files_setup_parser,
    command_kwargs={"help": "Uploads a file or directory for a specific dataset."},
)

download_files_command = RobotoCommand(
    name="download-files",
    logic=download_files,
    setup_parser=download_files_setup_parser,
    command_kwargs={"help": "Downloads a file or directory for a specific dataset."},
)

commands = [
    create_command,
    get_command,
    query_command,
    list_files_command,
    upload_files_command,
    download_files_command,
]

command_set = RobotoCommandSet(
    name="datasets",
    help="Get, create, update, and query datasets. Upload to and download from them.",
    commands=commands,
)
