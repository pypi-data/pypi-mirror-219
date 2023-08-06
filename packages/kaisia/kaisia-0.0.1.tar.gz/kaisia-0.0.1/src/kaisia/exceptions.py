from .cli import Colors


class MissingConfig(Exception):
    """Exception raised for errors in the config object.

    Attributes:
        param -- configuration parameter
        message -- explanation of the error
    """

    def __init__(self, param, message="Missing config parameter"):
        super().__init__(f"{message}: {Colors.FAIL}{param}")


class IncorrectID(Exception):
    """Exception raised for errors in the gbq parsing of ids.

    Attributes:
        id -- user input id
        message -- explanation of the error
    """

    def __init__(self, id, reason: str = "", message: str = "Parsing faled"):
        super().__init__(
            f"{message} {'with ' + reason if reason else ''}: {Colors.FAIL}{id}"
        )


class TooManyTables(Exception):
    """Exception raised for errors in the amoutn of input tables

    Attributes:
        tables_count -- amount of tables
        message -- explanation of the error
    """

    def __init__(
        self, tables_count, message: str = "Processing faled - too many tables"
    ):
        super().__init__(f"{message}: {Colors.FAIL}{tables_count}")
