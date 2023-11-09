# -*- coding: utf-8 -*-
# File: config.py

from typing import Any, Iterator

from .file_ops import get_file_ext, read_file
from .types import PathLike

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
        json_path (PathLike): Path to .json

    Returns:
        Any: Loaded .json
    """

    assert get_file_ext(json_path).lower() == ".json", ".json required"

    import json

    with open(json_path, "r") as f_json:
        return json.load(f_json)
    

def load_jsonl(jsonl_path: PathLike) -> Iterator[Any]:
    """
    Load a .jsonl file.

    Args:
        jsonl_path (PathLike): Path to .jsonl

    Returns:
        Iterator[Any]: Loaded .jsonl
    """

    assert get_file_ext(jsonl_path).lower() == ".jsonl", ".jsonl required"

    import json

    for line in read_file(jsonl_path):
        yield json.loads(line)


def load_yaml(yaml_path: PathLike, safe: bool = True) -> Any:
    """
    Load a .yaml file.

    Args:
        yaml_path (PathLike): Path to .yaml
        safe (bool, optional): Load `yaml_path` safely. Defaults to True.

    Returns:
        Any: Loaded .yaml
    """

    assert get_file_ext(yaml_path).lower() == ".yaml", ".yaml required"

    try:
        import yaml
    except ImportError:
        raise ImportError("Could not import yaml. Try `pip install -U pyyaml`.")
    
    with open(yaml_path, "r") as f_yaml:
        return yaml.safe_load(f_yaml) if safe else yaml.load(f_yaml)
    

def load_ini(ini_path: PathLike) -> Any:
    """
    Load a .ini file.

    Args:
        ini_path (PathLike): Path to .ini

    Returns:
        ConfigParser: Loaded .ini
    """

    def _load_ini(ini_path: PathLike) -> ConfigParser:
        config = ConfigParser()
        config.read(ini_path)

        return config
    
    assert get_file_ext(ini_path).lower() == ".ini", ".ini required"

    from configparser import ConfigParser

    return _load_ini(ini_path)


def load_xml(xml_path: PathLike) -> Any:
    """
    Load a .xml file.

    Args:
        xml_path (PathLike): Path to .xml

    Returns:
        BeautifulSoup: Loaded .xml
    """

    def _load_xml(xml_path: PathLike) -> BeautifulSoup:
        with open(xml_path, "r") as f_xml:
            return BeautifulSoup(f_xml.read(), features="html.parser")
        
    assert get_file_ext(xml_path).lower() == ".xml", ".xml required"

    from bs4 import BeautifulSoup

    return _load_xml(xml_path)
