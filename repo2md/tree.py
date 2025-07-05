import os
import pathlib

from typing import Sequence

IGNORE_LIST = (
    "__pycache__",
    ".git",
    ".idea",
    "venv",
    ".github",
    "node_modules",
    ".ds_store",
    ".vscode",
    ".pytest_cache",
    "build",
    "dist",
    "docs",
    "tests",
    "gradle"
)


class Tree:
    """A class to generate a tree structure of directories and files.

    >>> Tree

    """

    def __init__(self, path: pathlib.Path, ignore: Sequence[str] = IGNORE_LIST):
        """Initialize the Tree with a path and optional ignore list.

        Args:
            path: The root path to start building the tree.
            ignore: Files and directories to ignore in the tree structure.
        """
        self.__tree = []
        self.path = pathlib.Path(path)
        self.ignore = ignore

    def get(self) -> str:
        """Generate the tree structure starting from the specified path."""
        self.__tree.clear()
        self.__get(self.path)
        return "\n".join(self.__tree)

    def __get(self, path: pathlib.Path, last: bool = True, header: str = ""):
        """Recursively build the tree structure for the given path.

        Args:
            path: The current path to process.
            last: Whether this is the last item in the current directory.
            header: The header string to prepend to the current line.
        """
        # If the current path should be ignored, return early
        for i in self.ignore:
            if i in path.name:
                return

        # Symbols for the tree
        elbow = "└──"
        pipe = "│  "
        tee = "├──"
        blank = "   "

        # Handle the current directory name (check if it's the root or current directory)
        if path == pathlib.Path("."):
            folder_name = os.getcwd().split("/")[-1]
        else:
            # If it's a directory with a name, use path.name; else, fall back to path.parts[-1]
            folder_name = path.name if path.name else path.parts[-1]

        # Append the folder name with the appropriate tree symbol
        self.__tree.append(header + (elbow if last else tee) + folder_name)

        # If the current path is a directory, recurse into its contents
        if path.is_dir():
            children = list(path.iterdir())

            # Filter out ignored files and folders
            children = [
                child
                for child in children
                if not any(ignored in child.name for ignored in self.ignore)
            ]

            for i, c in enumerate(children):
                # Pass the correct `last` flag based on whether this is the last child in the filtered list
                self.__get(
                    c,
                    last=i == len(children) - 1,
                    header=header + (blank if last else pipe),
                )


if __name__ == "__main__":
    tree = Tree(pathlib.Path("."))
    print(tree.get())
