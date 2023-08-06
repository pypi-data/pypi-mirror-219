import ast
from typing import Any, Generator, Tuple, Type
import importlib.metadata as importlib_metadata


def get_r_index(line: str) -> int:
    try:
        return line.index("\r")
    except ValueError:
        return -1


class EOLChecker:
    name = "flake8-eol"
    version = importlib_metadata.version(name)

    def __init__(self, tree: ast.AST, filename: str) -> None:
        self.tree = tree
        self.filename = filename

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        with open(self.filename, "r", newline="") as f:
            for n, line in enumerate(f, 1):
                r_index = get_r_index(line)
                if r_index != -1:
                    yield (
                        n,
                        r_index + 1,
                        "EOL001 make sure to use '\\n' instead of '\\r\\n' or '\\r'",
                        type(self),
                    )
