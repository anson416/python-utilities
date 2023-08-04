# -*- coding: utf-8 -*-
# File: utils.py

import os
import tarfile
import zipfile
from typing import Any, Optional

from . import beartype
from .file_ops import get_basename, remove_file
from .types import Pathlike, StrDict

__all__ = [
    "has_package",
    "load_config",
    "extract_file",
]


@beartype
def has_package(
    package_name: str,
    raise_err: bool = False,
) -> bool:
    """
    Return True if a package is installed in the current environment.

    Args:
        package_name (str): Name of package
        raise_err (bool, optional): If True, raise ImportError if `package_name` is not found

    Raises:
        ImportError: Raise iff `raise_err` == True and `package_name` is not found

    Returns:
        bool: True iff package_name is found
    """

    import importlib.util

    if importlib.util.find_spec(package_name):
        return True
    else:
        if raise_err:
            raise ImportError(f"Package \"{package_name}\" not found")
        else:
            return False


@beartype
def load_config(config_path: Pathlike) -> StrDict[Any]:
    """
    Load a .json or .yaml file.

    Args:
        config_path (Pathlike): Target file

    Returns:
        StrDict[Any]: Dictionary loaded from `config_path`
    """

    ext = get_basename(config_path, split_ext=True)[1].lower()
    with open(config_path, "r") as f:
        if ext == ".json":
            import json

            return json.load(f)
        elif ext == ".yaml":
            try:
                import yaml
            except ImportError:
                raise ImportError("Could not import yaml. Try `pip3 install -U pyyaml`.")

            return yaml.safe_load(f)
        else:
            raise ValueError(f"{ext} is not supported")


@beartype
def extract_file(
    file_path: Pathlike,
    dir: Optional[Pathlike] = None,
    replace_existing: bool = True,
    remove_archive: bool = False,
) -> tuple[Pathlike, list[Pathlike]]:
    """
    Extract files from an archive.

    Args:
        file_path (Pathlike): Target file
        dir (Optional[Pathlike], optional): If not None, extract archive to dir. Defaults to "./".
        replace_existing (bool, optional): If True, replace the existing file if a file with the same name already \
            exists. Defaults to True.
        remove_archive (bool, optional): If True, remove the archive after all files are extracted. Defaults to False.

    Returns:
        tuple[Pathlike, list[Pathlike]]: Directory to extracted archive and paths to extracted files
    """

    file_name, ext = get_basename(file_path, split_ext=True)
    ext = ext.lower()
    output_dir = os.path.join(dir, file_name) if dir else os.path.join(".", file_name)
    extracted_files = None

    if ext == ".zip":
        with zipfile.ZipFile(file_path, "r") as f_zip:
            members = f_zip.namelist()
            extracted_files = list(map(lambda x: os.path.join(output_dir, x), members))
            for file in extracted_files:
                if not(not replace_existing and os.path.exists(file)):
                    f_zip.extract(get_basename(file), path=output_dir)
    elif "tar" in ext:
        mode = "r:" if ext == ".tar" else f"r:{ext.rsplit('.', 1)[1]}"
        with tarfile.open(file_path, mode) as f_tar:
            members = f_tar.getnames()
            extracted_files = list(map(lambda x: os.path.join(output_dir, x), members))
            for file in extracted_files:
                if not(not replace_existing and os.path.exists(file)):
                    f_tar.extract(get_basename(file), path=output_dir)
    else:
        raise ValueError(f"{ext} is not supported")

    if remove_archive:
        remove_file(file_path)

    return output_dir, extracted_files
