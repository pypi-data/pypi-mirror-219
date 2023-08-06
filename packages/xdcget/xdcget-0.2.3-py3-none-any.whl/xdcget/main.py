"""
Command line options and xdcget subcommand wrapper.
"""
import sys
import argparse
from pathlib import Path

from termcolor import colored

from .config import read_config, write_initial_config
from .storage import perform_update, perform_export, perform_status


class Out:
    def red(self, msg):
        print(colored(msg, "red"))

    def green(self, msg):
        print(colored(msg, "green"))

    def __call__(self, msg, red=False, green=False):
        color = "red" if red else ("green" if green else None)
        print(colored(msg, color))


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--toml",
        type=Path,
        dest="xdcget_ini",
        default=Path("xdcget.ini"),
        help="path to xdcget.ini file (defaults to look in current directory)",
    )
    subparsers = parser.add_subparsers(
        title="subcommands", description="valid subcommands", required=True
    )

    def add(func):
        name = func.__name__
        assert name.endswith("_cmd")
        name = name[:-4]
        doc = func.__doc__.strip()
        p = subparsers.add_parser(name, description=doc)
        p.set_defaults(func=func)
        return p

    add(init_cmd)
    add(update_cmd)
    add(status_cmd)
    add(export_cmd)

    return parser


def init_cmd(args, out):
    """initialize config and sources template file if it doesn't exist"""
    if args.xdcget_ini.exists():
        out.red(f"Path exists, not modifying: {args.xdcget_ini}")
        raise SystemExit(1)
    write_initial_config(args.xdcget_ini, out)
    out.green(f"created -- please inspect: {args.xdcget_ini}")


def update_cmd(args, out):
    """update webxdc app files from release resources"""
    config = read_config(args.xdcget_ini)
    perform_update(config, out)


def status_cmd(args, out):
    """show app index status."""
    config = read_config(args.xdcget_ini)
    perform_status(config, out)


def export_cmd(args, out):
    """export release files for use with 'xdcstore' import"""
    config = read_config(args.xdcget_ini)
    perform_export(config, out)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = get_parser()
    args = parser.parse_args(argv)
    out = Out()
    args.func(args, out)


if __name__ == "__main__":
    main()
