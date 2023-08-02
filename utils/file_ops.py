# -*- coding: utf-8 -*-
# File: file_ops.py

import os
import shutil
from typing import Optional, Union

from . import beartype
from .types import Array, Pathlike

__all__ = ["get_basename",
           "get_file_size",
           "get_parent_dir",
           "create_dir",
           "remove_dir",
           "remove_file",
           "list_files",
           "read_file"]


@beartype
def get_basename(
    file_path: Pathlike,
    split_ext: bool = False,
) -> Union[str, tuple[str, str]]:
    """
    Get either basename or file name and extension of a file.

    Args:
        file_path (Pathlike): Target file
        split_ext (bool, optional): If True, split extension from basename, creating a 2-tuple. Defaults to False.

    Returns:
        Union[str, tuple[str, str]]: Either basename or file name and extension of a file
    """

    basename = os.path.basename(file_path)

    return os.path.splitext(basename) if split_ext else basename


@beartype
def get_file_size(file_path: Pathlike) -> int:
    """
    Get the size of a file.

    Args:
        file_path (Pathlike): Target file

    Returns:
        int: File size (in bytes)
    """

    return os.path.getsize(file_path)


@beartype
def get_parent_dir(file_path: Pathlike) -> Pathlike:
    """
    Get the parent directory of a file. To get the parent directory of any Python script, do get_parent_dir(__file__).

    Args:
        file_path (Pathlike): Target file

    Returns:
        Pathlike: Parent directory
    """

    return os.path.dirname(os.path.abspath(file_path))


@beartype
def create_dir(dir: Pathlike, remove_existing: bool = False) -> None:
    """
    Create a tree of directory.

    Args:
        dir (Pathlike): Target directory
        remove_existing (bool): If True, remove existing directory before creation. Defaults to False.
    """

    if remove_existing:
        remove_dir(dir)
        
    os.makedirs(dir, exist_ok=True)


@beartype
def remove_dir(dir: Pathlike, only_empty: bool = False) -> bool:
    """
    Remove a directory.

    Args:
        dir (Pathlike): Target directory
        only_empty (bool, optional): If True, remove dir only if it is empty. Defaults to False.

    Returns:
        bool: True iff the directory is removed
    """

    removed = False

    if os.path.exists(dir):
        os.rmdir(dir) if only_empty else shutil.rmtree(dir)
        removed = True

    return removed


@beartype
def remove_file(file_path: Pathlike) -> bool:
    """
    Remove a file if it exists.

    Args:
        file_path (Pathlike): Target file

    Returns:
        bool: True iff the file is removed
    """

    removed = False

    if os.path.exists(file_path):
        os.remove(file_path)
        removed = True

    return removed


@beartype
def list_files(
    dir: Pathlike,
    exts: Optional[Union[Array[str], str]] = None,
    base_only: bool = False
) -> list[str]:
    """
    Get all file paths or names under a directory recursively. Similar to the ls command on Linux.

    Args:
        dir (Pathlike): Target directory
        exts (Optional[Union[Array[str], str]], optional): If not None, return a file only if its extension is in \
            exts. Defaults to None.
        base_only (bool, optional): If True, return only basename, not the entire path. Defaults to False.

    Returns:
        list[str]: File paths or names
    """

    if isinstance(exts, str):
        exts = (exts,)

    files = []

    for item in os.listdir(dir):
        item_path = os.path.join(dir, item)
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


@beartype
def read_file(file_path: Pathlike, remove_spaces: bool = False, remove_empty: bool = False) -> list[str]:
    """
    Read lines from a file (with formatting).

    Args:
        file_path (Pathlike): Target file
        remove_spaces (bool, optional): If True, remove leading and trailing whitespaces. Defaults to False.
        remove_empty (bool, optional): If True, neglect empty lines. Defaults to False.

    Returns:
        list[str]: Lines in a file
    """

    with open(file_path, "r") as f:
        lines = list(map(lambda x: x.rstrip("\n"), f.readlines()))

    if remove_spaces:
        lines = list(map(lambda x: x.strip(), lines))

    if remove_empty:
        lines = [line for line in lines if line != ""]

    return lines
