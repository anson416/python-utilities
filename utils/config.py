# -*- coding: utf-8 -*-
# File: utils/config.py

from pathlib import Path
from typing import Any, Iterator

from .file_ops import get_file_ext, read_file
from .types_ import PathLike

__all__ = [
    "load_json",
    "load_jsonl",
    "load_yaml",
    "load_ini",
    "load_xml",
]


def load_json(json_path: PathLike) -> Any:
    """
    Load a .json file.

    Args:
        json_path (PathLike): Path to the .json file.

    Returns:
        Any: Python object loaded from `json_path`.
    """

    assert (
        get_file_ext(json_path := Path(json_path)).lower() == ".json"
    ), ".json required."
    import json

    with json_path.open() as f_json:
        return json.load(f_json)


def load_jsonl(jsonl_path: PathLike) -> Iterator[Any]:
    """
    Load a .jsonl file.

    Args:
        jsonl_path (PathLike): Path to the .jsonl file.

    Returns:
        Iterator[Any]: Python objects loaded from each line in `jsonl_path`.
    """

    assert (
        get_file_ext(jsonl_path := Path(jsonl_path)).lower() == ".jsonl"
    ), ".jsonl required."
    import json

    for line in read_file(jsonl_path):
        yield json.loads(line)


def load_yaml(yaml_path: PathLike, safe: bool = True) -> Any:
    """
    Load a .yaml file.

    Args:
        yaml_path (PathLike): Path to the .yaml file.
        safe (bool, optional): Load `yaml_path` safely. Defaults to True.

    Returns:
        Any: Python object loaded from `yaml_path`.
    """

    assert (
        get_file_ext(yaml_path := Path(yaml_path)).lower() == ".yaml"
    ), ".yaml required."
    try:
        import yaml
    except ImportError:
        raise ImportError("Could not import yaml. Try `pip install -U pyyaml`.")
    with yaml_path.open() as f_yaml:
        return yaml.safe_load(f_yaml) if safe else yaml.load(f_yaml)


def load_ini(ini_path: PathLike) -> Any:
    """
    Load a .ini file.

    Args:
        ini_path (PathLike): Path to the .ini file.

    Returns:
        ConfigParser: Loaded `ini_path`.
    """

    from configparser import ConfigParser

    def _load_ini(ini_path: PathLike) -> ConfigParser:
        config = ConfigParser()
        config.read(ini_path)
        return config

    assert get_file_ext(ini_path := Path(ini_path)).lower() == ".ini", ".ini required."
    return _load_ini(ini_path)


def load_xml(xml_path: PathLike) -> Any:
    """
    Load a .xml file.

    Args:
        xml_path (PathLike): Path to the .xml file.

    Returns:
        BeautifulSoup: Loaded `xml_path`.
    """

    from bs4 import BeautifulSoup

    def _load_xml(xml_path: PathLike) -> BeautifulSoup:
        with xml_path.open() as f_xml:
            return BeautifulSoup(f_xml.read(), features="html.parser")

    assert get_file_ext(xml_path := Path(xml_path)).lower() == ".xml", ".xml required."
    return _load_xml(xml_path)
