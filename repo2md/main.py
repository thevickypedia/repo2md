import os
import pathlib
from collections.abc import Generator
from typing import Dict, List, Tuple

from repo2md.tree import Tree
from repo2md.utils import (
    IGNORE_DIRECTORIES,
    IGNORE_FILES,
    LANGUAGE_EXTENSIONS,
    LOGGER,
)


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
        return {filepath: "\n".join([f.replace("\n", "") for f in fstream.readlines()])}


def get_current(
    dir_path: str, ignore_files: List[str], language: str = None
) -> Generator[Dict[str, str]]:
    """Loops through the current directory and yields file contents as dictionaries.

    Args:
        dir_path: Directory path to loop through.
        ignore_files: Files to ignore in the directory.
        language: Language to filter files.

    Yields:
        Dict[str, str]:
        A dictionary with the file path as the key and the file content as the value.
    """
    LOGGER.info("Reading directory %s", dir_path)
    extensions = LANGUAGE_EXTENSIONS[language.lower()]
    for file in os.listdir(dir_path):
        if file.lower() in ignore_files:
            LOGGER.debug("Ignoring file %s in directory %s", file, dir_path)
            continue
        if language and pathlib.Path(file).suffix not in extensions:
            continue
        filepath = os.path.join(dir_path, file)
        if os.path.isfile(filepath):
            yield get_content(filepath)


def get_files(
    src: str,
    ignore_directories: List[str] = IGNORE_DIRECTORIES,
    ignore_files: List[str] = IGNORE_FILES,
    language: str = None,
) -> Generator[Tuple[str, List[Dict[str, str]]]]:
    """Walks through the source directory and yields directories with their file contents.

    Args:
        src: Source directory to walk through.
        ignore_directories: Directories to ignore in the walk.
        ignore_files: Files to ignore in the directories.
        language: Language to filter files.

    Yields:
        Tuple[str, List[Dict[str, str]]]:
        A generator yielding tuples of directory paths and lists of dictionaries containing file contents.
    """
    LOGGER.info("Walking directory %s", src)
    for __path, directories, files in os.walk(src):
        if any((ignore in __path.lower() for ignore in ignore_directories)):
            LOGGER.debug("Ignoring directory %s", __path)
            continue
        # Loops through root directory
        if __path == src:
            yield src, list(get_current(src, ignore_files, language))
        # Loops through subdirectories
        for directory in directories:
            if directory.lower() in ignore_directories:
                LOGGER.debug("Ignoring directory %s", directory)
                continue
            dir_path = os.path.join(__path, directory)
            yield dir_path, list(get_current(dir_path, ignore_files, language))


def get_code(iterator: Generator[Tuple[str, List[Dict[str, str]]]]) -> str:
    """Generates a formatted string of code contents from the iterator.

    Args:
        iterator: Iterator yielding directory paths and lists of file contents.

    Returns:
        str:
        A formatted string containing the code contents, either in Markdown format or plain text.
    """
    text = ""
    for __dir, content_list in iterator:
        for file_content_map in content_list:
            for filepath, content in file_content_map.items():
                text += f"###### {filepath}\n\n"
                text += f"```\n{content.strip()}\n```"
                text += "\n\n"
    return text


def generate_markdown(
    path: str | pathlib.Path | os.PathLike, filename: str, language: str = None
) -> None:
    """Generates a Markdown file with the directory tree and code contents.

    Args:
        path: Path to the directory to process.
        filename: Filename for the output Markdown file.
        language: Programming language of the code files.
    """
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)
    assert path.exists(), f"Path {path.name} at {path.parent} does not exist"
    if not filename:
        filename = f"{path.name}.md"
    iterator = get_files(str(path), language=language)
    text = get_code(iterator)
    LOGGER.info("Generating tree for %s", path)
    tree = Tree(path).get()
    LOGGER.info("Storing output in %s", filename)
    with open(filename, "w") as file:
        file.write(f"## Contents:\n\n```\n{tree}\n```\n\n")
        file.write(text.rstrip())
        file.write("\n")
        file.flush()
