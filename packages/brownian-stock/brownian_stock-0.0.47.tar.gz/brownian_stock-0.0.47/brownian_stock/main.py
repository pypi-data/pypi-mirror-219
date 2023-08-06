import argparse
import logging
import sys
from typing import List, Optional

from .commands import download, generate


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Subcommand Download
    parser_download = subparsers.add_parser("download", description="Download stock information from KABU+")
    parser_download.add_argument("--dir_path", type=str)
    parser_download.add_argument("--db_connection", type=str)
    parser_download.add_argument("--s3_bucket", type=str)
    parser_download.add_argument("--limit", type=int)
    parser_download.add_argument("--config", type=str)
    parser_download.add_argument("--only_brand", action="store_true")
    parser_download.add_argument("--only_stock", action="store_true")
    parser_download.add_argument("--only_statements", action="store_true")
    parser_download.add_argument("--only_yahoo", action="store_true")
    parser_download.add_argument("--only_margin_interests", action="store_true")
    parser_download.add_argument("--dot_file", type=str)
    parser_download.add_argument("--force", action="store_true", help="Force to download all contents")
    parser_download.add_argument("--interval", type=int, default=1, help="Interval between each downloads.")
    parser_download.add_argument("--username", type=str)
    parser_download.add_argument("--password", type=str)
    parser_download.set_defaults(handler=command_download)

    # Subcommand generate
    parser_preprocess = subparsers.add_parser("generate", description="Build dataset")
    parser_preprocess.add_argument("--dir_path", type=str)
    parser_preprocess.add_argument("--s3_bucket", type=str)
    parser_preprocess.add_argument("--db_connection", type=str)
    parser_preprocess.add_argument("--config", type=str)
    parser_preprocess.add_argument("--limit", type=int)
    parser_preprocess.add_argument("--generate_csv", action="store_true")
    parser_preprocess.set_defaults(handler=command_generate)
    return parser


def command_download(args: argparse.Namespace) -> None:
    logging.basicConfig(level=logging.INFO)
    download.run_download(args)


def command_generate(args: argparse.Namespace) -> None:
    logging.basicConfig(level=logging.INFO)
    generate.run_generate(args)


def main(args_list: Optional[List[str]] = None) -> None:
    parser = get_parser()

    if args_list is None:
        args_list = sys.argv[1:]

    args = parser.parse_args(args_list)
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
