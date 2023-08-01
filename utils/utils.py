# -*- coding: utf-8 -*-
# File: utils.py

import importlib.util
import json
import os
import tarfile
import urllib.request
import zipfile
from datetime import datetime
from typing import Any, Optional

from . import beartype
from .error import err2str, raise_err
from .file_ops import get_basename, remove_file
from .logger import logger
from .types import Pathlike, StrDict

__all__ = ["get_datetime",
           "load_config",
           "download_file",
           "extract_file",
           "is_package_installed"]


@beartype
def get_datetime(datetime_sep: str = " ", date_sep: str = "-", time_sep: str = ":") -> str:
    """
    Return formatted date and time.

    Args:
        datetime_sep (str, optional): Separator between date and time. Defaults to " ".
        date_sep (str, optional): Separator between elements in date. Defaults to "-".
        time_sep (str, optional): Separator between elements in time. Defaults to ":".

    Returns:
        str: Date and time

    Examples:
        get_datetime(datetime_sep="_", date_sep="", time_sep="-") -> 20230101_08-02-47
    """

    date_format = f"%Y{date_sep}%m{date_sep}%d"
    time_format = f"%H{time_sep}%M{time_sep}%S"
    
    return datetime.now().strftime(f"{date_format}{datetime_sep}{time_format}")


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
            except ImportError as e:
                err_msg = f"Cannot import yaml. Try `pip install -U pyyaml`. ({err2str(e)})"
                logger.error(err_msg)
                raise_err(e, msg=err_msg)

            return yaml.safe_load(f)
        else:
            err_msg = f"{ext} is not supported"
            logger.error(err_msg)
            raise ValueError(err_msg)


@beartype
def download_file(
        url: str, dir: Optional[Pathlike] = None, file_name: Optional[str] = None, replace_existing: bool = True,
        show_progress_bar: bool = True) -> tuple[Pathlike, int]:
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
            except ImportError as e:
                err_msg = f"Cannot import tqdm. Try `pip install -U tqdm`. ({err2str(e)})"
                logger.error(err_msg)
                raise_err(e, msg=err_msg)
                
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
        file_path: Pathlike, dir: Optional[Pathlike] = None, replace_existing: bool = True,
        remove_archive: bool = False) -> tuple[Pathlike, list[Pathlike]]:
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
        err_msg = f"{ext} is not supported"
        logger.error(err_msg)
        raise ValueError(err_msg)

    if remove_archive:
        remove_file(file_path)

    return output_dir, extracted_files


@beartype
def is_package_installed(package_name: str) -> bool:
    """
    Return True if a package is installed in the current environment.

    Args:
        package_name (str): Name of package

    Returns:
        bool: True if the package is installed
    """
    
    return importlib.util.find_spec(package_name) != None
