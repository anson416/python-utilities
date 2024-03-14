# -*- coding: utf-8 -*-
# File: utils/file_ops.py

from pathlib import Path
from typing import Iterator, List, Optional, Set

from .types_ import PathLike

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
    "get_abs_path",
    "create_dir",
    "remove_dir",
    "remove_file",
    "get_cwd",
    "get_home",
    "list_files",
    "read_file",
    "copy_file",
]


def exists(path: PathLike) -> bool:
    """
    Return True if a path exists.

    Args:
        path (PathLike): Target path.

    Returns:
        bool: True if `path` exists.
    """

    return Path(path).exists()


def is_dir(path: PathLike) -> bool:
    """
    Return True if a path is a directory.

    Args:
        path (PathLike): Target path.

    Returns:
        bool: True if `path` is a directory.
    """

    return Path(path).is_dir()


def is_file(path: PathLike) -> bool:
    """
    Return True if a path is a regular file.

    Args:
        path (PathLike): Target path.

    Returns:
        bool: True if `path` is a regular file.
    """

    return Path(path).is_file()


def get_basename(path: PathLike) -> str:
    """
    Get the basename of a file.

    Args:
        path (PathLike): Target file.

    Returns:
        str: Basename of a file.
    """

    return Path(path).name


def get_filename(path: PathLike) -> str:
    """
    Get the file name of a file.

    Args:
        path (PathLike): Target file.

    Returns:
        str: File name of a file.
    """

    return Path(path).stem


def get_file_ext(path: PathLike) -> str:
    """
    Get the file extension (including leading period) of a file.

    Args:
        path (PathLike): Target file.

    Returns:
        str: File extension of a file.
    """

    return Path(path).suffix


def get_file_exts(path: PathLike) -> List[str]:
    """
    Get the list of file extensions (including leading period) of a file.

    Args:
        path (PathLike): Target file.

    Returns:
        List[str]: List of file extensions of a file.
    """

    return Path(path).suffixes


def get_file_size(path: PathLike) -> int:
    """
    Get the size of a file.

    Args:
        path (PathLike): Target file.

    Returns:
        int: File size (in bytes).
    """

    return Path(path).stat().st_size


def get_parent(path: PathLike) -> Path:
    """
    Get the parent directory of a file. To get the parent directory of any
    Python script, do get_parent(__file__).

    Args:
        path (PathLike): Target file.

    Returns:
        Path: Parent directory.
    """

    return Path(path).parent


def get_abs_path(path: PathLike) -> Path:
    """
    Get the absolute path of a path.

    Args:
        path (PathLike): Target path.

    Returns:
        Path: Absolute path of `path`.
    """

    return Path(path).resolve()


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
        tgt_dir (PathLike): Target directory.
        remove_existing (bool, optional): Remove existing `tgt_dir` (if any)
            before creation. Defaults to False.
        build_tree (bool, optional): Create a leaf directory and all
            intermediate ones. Defaults to True.
        exist_ok (bool, optional): Raise an OSError if `tgt_dir` already
            exists. Defaults to False.
        mode (int, optional): Set the file mode and access flags. Defaults to
            511.

    Returns:
        bool: True if `tgt_dir` is created.
    """

    if remove_existing:
        remove_dir(tgt_dir)
    try:
        Path(tgt_dir).mkdir(mode=mode, parents=build_tree, exist_ok=exist_ok)
        return True
    except:
        return False


def remove_dir(
    tgt_dir: PathLike,
    only_empty: bool = False,
) -> bool:
    """
    Remove a directory.

    Args:
        tgt_dir (PathLike): Target directory.
        only_empty (bool, optional): Remove `tgt_dir` only if it is empty.
            Defaults to False.

    Returns:
        bool: True if `tgt_dir` is removed.
    """

    import shutil

    if exists(tgt_dir := Path(tgt_dir)):
        if not is_dir(tgt_dir):
            raise NotADirectoryError(f"{str(tgt_dir)} is not a directory. `tgt_dir` must be a directory")
        tgt_dir.rmdir() if only_empty else shutil.rmtree(tgt_dir)
        return True
    return False


def remove_file(path: PathLike) -> bool:
    """
    Remove a file if it exists.

    Args:
        path (PathLike): Target file.

    Returns:
        bool: True if `path` is removed.
    """

    if exists(path := Path(path)):
        if not is_file(path):
            raise OSError(f"{str(path)} is not a regular file. `path` must be a regular file.")
        path.unlink()
        return True
    return False


def get_cwd() -> Path:
    """
    Get the current working directory (CWD).

    Returns:
        Path: CWD.
    """

    return Path.cwd()


def get_home() -> Path:
    """
    Get the user's home directory.

    Returns:
        Path: User's home directory.
    """

    return Path.home()


def list_files(
    tgt_dir: PathLike,
    exts: Optional[Set[str]] = None,
    case_insensitive: bool = False,
    recursive: bool = False,
) -> Iterator[Path]:
    """
    Get all file paths under a directory (recursively). Similar to the `ls -a`
    (`ls -R` for recursive directory listing) command on Linux.

    Args:
        tgt_dir (PathLike): Target directory.
        exts (Optional[Set[str]], optional): If not None, return a file path
            only if its extension (including leading period) is in `exts`.
            Defaults to None.
        case_insensitive (bool, optional): Neglect case of file extensions.
            Used only if `exts` is not None. Defaults to False.
        recursive (bool, optional): Recurse into sub-directories. Defaults to
            False.

    Returns:
        Iterator[Path]: File paths under `tgt_dir`.
    """

    exts = set(map(lambda x: x.lower(), exts)) if exts is not None and case_insensitive else exts
    for child in (tgt_dir := Path(tgt_dir)).iterdir():
        if is_file(child):
            if exts is not None:
                ext = get_file_ext(child)
                if (ext.lower() if case_insensitive else ext) in exts:
                    yield child
            else:
                yield child
        elif is_dir(child):
            if recursive:
                yield from list_files(child, exts=exts, case_insensitive=case_insensitive, recursive=recursive)


def read_file(
    path: PathLike,
    remove_spaces: bool = False,
    remove_empty: bool = False,
) -> Iterator[str]:
    """
    Read lines from a file (with formatting).

    Args:
        path (PathLike): Target file.
        remove_spaces (bool, optional): Remove leading and trailing
            whitespaces. Defaults to False.
        remove_empty (bool, optional): Omit empty lines. Defaults to False.

    Returns:
        Iterator[str]: Lines from `path`.
    """

    with Path(path).open() as f:
        for line in f:
            line = line.rstrip("\n")
            line = line.strip() if remove_spaces else line
            if remove_empty and line == "":
                continue
            yield line


def copy_file(
    src: PathLike,
    dst: PathLike,
) -> None:
    """
    Copy a file.

    Args:
        src (PathLike): Source path. Must be a file.
        dst (PathLike): Destination path. Can be a file or directory.
    """

    import shutil

    shutil.copy(src, dst)
