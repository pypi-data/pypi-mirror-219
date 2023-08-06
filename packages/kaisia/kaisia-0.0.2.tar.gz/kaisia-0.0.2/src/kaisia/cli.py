import argparse


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def add_table1(parser: argparse.ArgumentParser, choices=None, default=None) -> None:
    parser.add_argument(
        "-t1",
        "--table1",
        choices=choices,
        default=default,
        help="Table1 full GBQ id",
    )


def add_table2(parser: argparse.ArgumentParser, choices=None, default=None) -> None:
    parser.add_argument(
        "-t2",
        "--table2",
        choices=choices,
        default=default,
        help="Table2 full GBQ id",
    )


def credentials(parser: argparse.ArgumentParser, choices=None, default=None) -> None:
    parser.add_argument(
        "-c",
        "--credentials",
        choices=choices,
        default=default,
        help="GCP Service Account key",
    )
