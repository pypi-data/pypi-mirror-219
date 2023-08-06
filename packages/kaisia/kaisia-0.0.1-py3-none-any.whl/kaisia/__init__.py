import argparse
import sys
from typing import Optional
from typing import Sequence

from .cli import add_table1, add_table2, credentials
from .version import VERSION
from .gbq import Table, Delta
from .exceptions import MissingConfig


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version", action="version", version=f"kaisia {VERSION}")

    add_table1(parser)
    add_table2(parser)
    credentials(parser)

    if len(argv) == 0:
        parser.parse_args(["--help"])

    args = parser.parse_args(argv)
    if not args.table1 or not args.table2:
        raise MissingConfig("2 input tables")

    delta = Delta(
        resources=[
            Table(id=args.table1, credential_path=args.credentials),
            Table(id=args.table2, credential_path=args.credentials),
        ]
    )
    delta.to_terminal()


if __name__ == "__main__":
    exit(main())
