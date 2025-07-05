import os
import pathlib
from collections.abc import Generator
from typing import Dict, List, Sequence, Tuple

from repo2md.tree import Tree
from repo2md.utils import LOGGER


def get_content(filepath: str) -> Dict[str, str]:
    """Reads the content of a file and returns it as a dictionary with the filepath as the key.

    Args:
        filepath: File path to read.

    Returns:
        Dict[str, str]:
        A dictionary with the file path as the key and the file content as the value.
    """
    LOGGER.info("Reading file %s", filepath)
    with open(filepath) as fstream:
        return {
            filepath: "\n".join([f.replace("\n", "") for f in fstream.readlines()])
        }


def get_current(
    dir_path: str, extensions: Sequence[str] = None
) -> Generator[Dict[str, str]]:
    """Loops through the current directory and yields file contents as dictionaries.

    Args:
        dir_path: Directory path to loop through.
        extensions: Sequence of file extensions to filter files.

    Yields:
        Dict[str, str]:
        A dictionary with the file path as the key and the file content as the value.
    """
    LOGGER.info("Reading directory %s", dir_path)
    for file in os.listdir(dir_path):
        if extensions and pathlib.Path(file).suffix not in extensions:
            continue
        filepath = os.path.join(dir_path, file)
        if os.path.isfile(filepath):
            yield get_content(filepath)


def get_files(
    src: str,
    extensions: Sequence[str] = None,
) -> Generator[Tuple[str, List[Dict[str, str]]]]:
    """Walks through the source directory and yields directories with their file contents.

    Args:
        src: Source directory to walk through.
        extensions: Extensions of files to include in the output.

    Yields:
        Tuple[str, List[Dict[str, str]]]:
        A generator yielding tuples of directory paths and lists of dictionaries containing file contents.
    """
    LOGGER.info("Walking directory %s", src)
    for __path, directories, files in os.walk(src):
        # Loops through root directory
        if __path == src:
            yield src, list(get_current(src, extensions))
        # Loops through subdirectories
        for directory in directories:
            dir_path = os.path.join(__path, directory)
            yield dir_path, list(get_current(dir_path, extensions))


def get_code(
    iterator: Generator[Tuple[str, List[Dict[str, str]]]], markdown: bool = False
) -> str:
    """Generates a formatted string of code contents from the iterator.

    Args:
        iterator: Iterator yielding directory paths and lists of file contents.
        markdown: Boolean flag to format the output as Markdown.

    Returns:
        str:
        A formatted string containing the code contents, either in Markdown format or plain text.
    """
    text = ""
    for __dir, content_list in iterator:
        for file_content_map in content_list:
            for filepath, content in file_content_map.items():
                text += f"###### {filepath}\n\n" if markdown else f"-- {filepath}\n\n"
                text += f"```\n{content.strip()}\n```" if markdown else content.strip()
                text += "\n\n"
    return text


def generate_markdown(
    path: str | pathlib.Path | os.PathLike,
    filename: str = None,
    extensions: Sequence[str] = None,
) -> None:
    """Generates a Markdown file with the directory tree and code contents.

    Args:
        path: Path to the directory to process.
        filename: Filename for the output Markdown file.
        extensions: Sequence of file extensions to filter files.
    """
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)
    assert path.exists(), f"Path {path.name} at {path.parent} does not exist"
    if not filename:
        filename = f"{path.name}.md"
    iterator = get_files(str(path), extensions=extensions)
    text = get_code(iterator, markdown=True)
    LOGGER.info("Generating tree for %s", path)
    tree = Tree(path).get()
    LOGGER.info("Storing output in %s", filename)
    with open(filename, "w") as file:
        file.write(f"## Contents:\n\n```\n{tree}\n```\n\n")
        file.write(text.rstrip())
        file.write("\n")
        file.flush()
