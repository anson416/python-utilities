# -*- coding: utf-8 -*-
# File: utils.py

import importlib.util
import json
import os
import tarfile
import urllib.request
import zipfile
from typing import Any, Optional

from . import beartype
from .file_ops import get_basename, remove_file
from .types import Pathlike, StrDict

__all__ = ["load_config",
           "download_file",
           "extract_file",
           "has_package"]


@beartype
def load_config(config_path: Pathlike) -> StrDict[Any]:
    """
    Load a .json or .yaml file.

    Args:
        config_path (Pathlike): Target file

    Returns:
        StrDict[Any]: Dictionary loaded from the file
    """

    ext = get_basename(config_path, split_ext=True)[1].lower()
    with open(config_path, "r") as f:
        if ext == ".json":
            return json.load(f)
        elif ext == ".yaml":
            try:
                import yaml
            except ImportError:
                raise ImportError("Cannot import yaml. Try `pip install -U pyyaml`.")

            return yaml.safe_load(f)
        else:
            raise ValueError(f"{ext} is not supported")


@beartype
def download_file(
    url: str,
    dir: Optional[Pathlike] = None,
    file_name: Optional[str] = None,
    replace_existing: bool = True,
    show_progress_bar: bool = True,
) -> tuple[Pathlike, int]:
    """
    Download a file from a URL.

    Args:
        url (str): Target URL
        dir (Optional[Pathlike], optional): If not None, download the file to dir. Defaults to "./".
        file_name (Optional[str], optional): If not None, save the file to file_name. Defaults to file name in url.
        replace_existing (bool, optional): If True, replace the existing file if a file with the same name already \
            exists. Defaults to True.
        show_progress_bar (bool, optional): If True, show a progress bar. Defaults to True.

    Returns:
        tuple[Pathlike, int]: Path to and size of downloaded file
    """

    download_dir = dir if dir else "./"
    file_path = os.path.join(
        download_dir, f"{file_name}{get_basename(url, split_ext=True)[1]}" if file_name else get_basename(url))

    # Get info from url
    response = urllib.request.urlopen(url)
    file_size = int(response.headers.get("Content-Length", 0))

    if not(not replace_existing and os.path.exists(file_path)):
        if show_progress_bar:  # Download with progress bar
            try:
                from tqdm import tqdm
            except ImportError:
                raise ImportError("Cannot import tqdm. Try `pip install -U tqdm`.")
                
            with tqdm(
                    total=file_size, unit="B", unit_scale=True, unit_divisor=1024, miniters=1, mininterval=0.1,
                    desc=file_path) as progress_bar:
                urllib.request.urlretrieve(
                    url, filename=file_path,
                    reporthook=lambda blocknum, blocksize, totalsize: progress_bar.update(blocksize))
        else:  # Download without progress bar
            urllib.request.urlretrieve(url, filename=file_path)
        
    return file_path, file_size


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


@beartype
def has_package(package_name: str, raise_err: bool = False) -> bool:
    """
    Return True if a package is installed in the current environment.

    Args:
        package_name (str): Name of package
        raise_err (bool, optional): If True, raise ImportError if package_name is not found

    Raises:
        ImportError: Raise if raise_err == True and package_name is not found

    Returns:
        bool: True iff package_name is found
    """

    if importlib.util.find_spec(package_name):
        return True
    else:
        if raise_err:
            raise ImportError(f"package \"{package_name}\" not found")
        else:
            return False
