# -*- coding: utf-8 -*-
# File: file_ops.py

from pathlib import Path
from typing import Iterator, List, Optional, Union

from .types_ import Array, PathLike

__all__ = [
    "exists",
    "is_dir",
    "is_file",
    "get_basename",
    "get_filename",
    "get_file_ext",
    "get_file_exts",
    "get_file_size",
    "get_parent",
    "create_dir",
    "remove_dir",
    "remove_file",
    "get_cwd",
    "get_home",
    "list_files",
    "read_file",
]


def exists(path: PathLike) -> bool:
    """
    Return True if a path exists.

    Args:
        path (PathLike): Target path

    Returns:
        bool: True if `path` exists
    """

    return Path(path).exists()


def is_dir(path: PathLike) -> bool:
    """
    Return True if a path is a directory.

    Args:
        path (PathLike): Target path

    Returns:
        bool: True if `path` is a directory
    """

    return Path(path).is_dir()


def is_file(path: PathLike) -> bool:
    """
    Return True if a path is a regular file.

    Args:
        path (PathLike): Target path

    Returns:
        bool: True if `path` is a regular file
    """
    
    return Path(path).is_file()


def get_basename(file_path: PathLike) -> str:
    """
    Get the basename of a file.

    Args:
        file_path (PathLike): Target file

    Returns:
        str: Basename of a file
    """

    return Path(file_path).name


def get_filename(file_path: PathLike) -> str:
    """
    Get the file name of a file.

    Args:
        file_path (PathLike): Target file

    Returns:
        str: File name of a file
    """

    return Path(file_path).stem


def get_file_ext(file_path: PathLike) -> str:
    """
    Get the file extension (including leading period) of a file.

    Args:
        file_path (PathLike): Target file

    Returns:
        str: File extension of a file
    """

    return Path(file_path).suffix


def get_file_exts(file_path: PathLike) -> List[str]:
    """
    Get the list of file extensions (including leading period) of a file.

    Args:
        file_path (PathLike): Target file

    Returns:
        List[str]: List of file extensions of a file
    """

    return Path(file_path).suffixes


def get_file_size(file_path: PathLike) -> int:
    """
    Get the size of a file.

    Args:
        file_path (PathLike): Target file

    Returns:
        int: File size (in bytes)
    """

    return Path(file_path).stat().st_size


def get_parent(file_path: PathLike) -> Path:
    """
    Get the parent directory of a file. To get the parent directory of any Python script, do get_parent(__file__).

    Args:
        file_path (PathLike): Target file

    Returns:
        Path: Parent directory
    """

    return Path(file_path).parent


def create_dir(
    tgt_dir: PathLike,
    remove_existing: bool = False,
    build_tree: bool = True,
    exist_ok: bool = False,
    mode: int = 511,
) -> bool:
    """
    Create a tree of directory.

    Args:
        tgt_dir (PathLike): Target directory
        remove_existing (bool, optional): Remove existing `tgt_dir` (if any) before creation. Defaults to False.
        build_tree (bool, optional): Create a leaf directory and all intermediate ones. Defaults to True.
        exist_ok (bool, optional): Raise an OSError if `tgt_dir` already exists. Defaults to False.
        mode (int, optional): Set the file mode and access flags. Defaults to 511.

    Returns:
        bool: True if `tgt_dir` is created
    """
    
    if remove_existing:
        remove_dir(tgt_dir)
    try:
        Path(tgt_dir).mkdir(mode=mode, parents=build_tree, exist_ok=exist_ok)
    except:
        return False
    
    return True


def remove_dir(
    tgt_dir: PathLike,
    only_empty: bool = False,
) -> bool:
    """
    Remove a directory.

    Args:
        tgt_dir (PathLike): Target directory
        only_empty (bool, optional): Remove `tgt_dir` only if it is empty. Defaults to False.

    Returns:
        bool: True if `tgt_dir` is removed
    """

    import shutil

    tgt_dir = Path(tgt_dir)
    if exists(tgt_dir):
        if not is_dir(tgt_dir):
            raise NotADirectoryError(f"{str(tgt_dir)} is not a directory. tgt_dir must be a directory")
        tgt_dir.rmdir() if only_empty else shutil.rmtree(tgt_dir)
        return True
    
    return False


def remove_file(file_path: PathLike) -> bool:
    """
    Remove a file if it exists.

    Args:
        file_path (PathLike): Target file

    Returns:
        bool: True if `file_path` is removed
    """

    file_path = Path(file_path)
    if exists(file_path):
        if not is_file(file_path):
            raise OSError(f"{str(file_path)} is not a regular file. file_path must be a regular file.")
        file_path.unlink()
        return True
    
    return False


def get_cwd() -> Path:
    """
    Get the current working directory (CWD).

    Returns:
        Path: CWD
    """

    return Path.cwd()


def get_home() -> Path:
    """
    Get the user's home directory.

    Returns:
        Path: User's home directory
    """
    
    return Path.home()


def list_files(
    tgt_dir: PathLike,
    exts: Optional[Union[Array[str], str]] = None,
    basename_only: bool = False,
) -> List[PathLike]:
    """
    Get all file paths or names under a directory recursively. Similar to the ls command on Linux.

    Args:
        tgt_dir (PathLike): Target directory
        exts (Optional[Union[Array[str], str]], optional): If not None, return a file only if its extension \
            (including leading period) is in `exts`. Defaults to None.
        basename_only (bool, optional): Return only basename, not the entire path. Defaults to False.

    Returns:
        List[PathLike]: File paths (Path) or basenames (str)
    """

    tgt_dir = Path(tgt_dir)
    if isinstance(exts, str):
        exts = (exts,)

    files = []
    for child in tgt_dir.iterdir():
        if is_file(child):
            file_path = get_basename(child) if basename_only else child
            if exts:
                if get_file_ext(file_path) in exts:
                    files.append(file_path)
            else:
                files.append(file_path)
        elif is_dir(child):
            files.extend(list_files(child, exts=exts, basename_only=basename_only))

    return files


def read_file(
    file_path: PathLike,
    remove_spaces: bool = False,
    remove_empty: bool = False,
) -> Iterator[str]:
    """
    Read lines from a file (with formatting).

    Args:
        file_path (PathLike): Target file
        remove_spaces (bool, optional): Remove leading and trailing whitespaces. Defaults to False.
        remove_empty (bool, optional): Omit empty lines. Defaults to False.

    Returns:
        Iterator[str]: Lines in a file
    """

    with Path(file_path).open() as f:
        for line in f:
            line = line.rstrip("\n")
            line = line.strip() if remove_spaces else line
            if remove_empty and line == "":
                continue
            yield line
