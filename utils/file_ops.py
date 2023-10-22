# -*- coding: utf-8 -*-
# File: file_ops.py

import os
from typing import Iterator, List, Optional, Tuple, Union

from .types import Array, Pathlike

__all__ = [
    "get_basename",
    "get_file_name",
    "get_file_ext",
    "get_file_size",
    "get_parent_dir",
    "create_dir",
    "remove_dir",
    "remove_file",
    "list_files",
    "read_file",
]


def get_basename(
    file_path: Pathlike,
    split_ext: bool = False,
) -> Union[str, Tuple[str, str]]:
    """
    Get either basename or file name and extension of a file.

    Args:
        file_path (Pathlike): Target file
        split_ext (bool, optional): Split extension from basename, creating a 2-tuple. Defaults to False.

    Returns:
        Union[str, Tuple[str, str]]: Either basename or file name and extension of a file
    """

    basename = os.path.basename(file_path)

    return os.path.splitext(basename) if split_ext else basename


def get_file_name(file_path: Pathlike) -> str:
    """
    Get file name of a file.

    Args:
        file_path (Pathlike): Target file

    Returns:
        str: File name of a file
    """

    return get_basename(file_path, split_ext=True)[0]


def get_file_ext(file_path: Pathlike) -> str:
    """
    Get file extension of a file.

    Args:
        file_path (Pathlike): Target file

    Returns:
        str: File extension of a file
    """

    return get_basename(file_path, split_ext=True)[1]


def get_file_size(file_path: Pathlike) -> int:
    """
    Get the size of a file.

    Args:
        file_path (Pathlike): Target file

    Returns:
        int: File size (in bytes)
    """

    return os.path.getsize(file_path)


def get_parent_dir(file_path: Pathlike) -> Pathlike:
    """
    Get the parent directory of a file. To get the parent directory of any Python script, do get_parent_dir(__file__).

    Args:
        file_path (Pathlike): Target file

    Returns:
        Pathlike: Parent directory
    """

    return os.path.dirname(os.path.abspath(file_path))


def create_dir(
    tgt_dir: Pathlike,
    remove_existing: bool = False,
) -> bool:
    """
    Create a tree of directory.

    Args:
        tgt_dir (Pathlike): Target directory
        remove_existing (bool, optional): Remove existing `tgt_dir` (if any) before creation. Defaults to False.

    Returns:
        bool: True if `tgt_dir` is created
    """

    if remove_existing:
        remove_dir(tgt_dir)
        
    try:
        os.makedirs(tgt_dir)
    except OSError:
        return False

    return True


def remove_dir(
    tgt_dir: Pathlike,
    only_empty: bool = False,
) -> bool:
    """
    Remove a directory.

    Args:
        tgt_dir (Pathlike): Target directory
        only_empty (bool, optional): Remove `tgt_dir` only if it is empty. Defaults to False.

    Returns:
        bool: True if `tgt_dir` is removed
    """

    import shutil

    removed = False

    if os.path.exists(tgt_dir):
        os.rmdir(tgt_dir) if only_empty else shutil.rmtree(tgt_dir)
        removed = True

    return removed


def remove_file(file_path: Pathlike) -> bool:
    """
    Remove a file if it exists.

    Args:
        file_path (Pathlike): Target file

    Returns:
        bool: True if `file_path` is removed
    """

    removed = False

    if os.path.exists(file_path):
        os.remove(file_path)
        removed = True

    return removed


def list_files(
    tgt_dir: Pathlike,
    exts: Optional[Union[Array[str], str]] = None,
    base_only: bool = False
) -> List[str]:
    """
    Get all file paths or names under a directory recursively. Similar to the ls command on Linux.

    Args:
        tgt_dir (Pathlike): Target directory
        exts (Optional[Union[Array[str], str]], optional): If not None, return a file only if its extension is in \
            `exts`. Defaults to None.
        base_only (bool, optional): Return only basename, not the entire path. Defaults to False.

    Returns:
        List[str]: File paths or names
    """

    if isinstance(exts, str):
        exts = (exts,)

    files = []

    for item in os.listdir(tgt_dir):
        item_path = os.path.join(tgt_dir, item)
        if os.path.isfile(item_path):
            file_path = item if base_only else item_path
            if exts:
                if get_basename(item_path, split_ext=True)[1] in exts:
                    files.append(file_path)
            else:
                files.append(file_path)
        elif os.path.isdir(item_path):
            files.extend(list_files(item_path, exts=exts, base_only=base_only))

    return files


def read_file(
    file_path: Pathlike,
    remove_spaces: bool = False,
    remove_empty: bool = False,
) -> Iterator[str]:
    """
    Read lines from a file (with formatting).

    Args:
        file_path (Pathlike): Target file
        remove_spaces (bool, optional): Remove leading and trailing whitespaces. Defaults to False.
        remove_empty (bool, optional): Omit empty lines. Defaults to False.

    Returns:
        Iterator[str]: Lines in a file
    """

    with open(file_path, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            line = line.strip() if remove_spaces else line
            if remove_empty and line == "":
                continue

            yield line
