import ast
import sys
from typing import Any, Generator, Tuple, Type

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


class EOLChecker:
    name = "flake8-eol"
    version = importlib_metadata.version(name)

    def __init__(self, tree: ast.AST, filename: str) -> None:
        self.tree = tree
        self.filename = filename

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        with open(self.filename, "rb") as f:
            first_line = f.readline()
            if first_line.endswith(b"\r\n"):
                yield (
                    1,
                    1,
                    "EOL001 '\\r\\n' at the end of the line is incorrect",
                    type(self),
                )
