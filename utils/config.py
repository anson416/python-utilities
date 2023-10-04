# -*- coding: utf-8 -*-
# File: config.py

from .file_ops import get_basename
from .types import Any, Iterator, Pathlike


def load_json(json_path: Pathlike) -> Any:
    """
    Load a .json file.

    Args:
        json_path (Pathlike): Path to .json

    Returns:
        Any: Loaded .json
    """

    assert get_basename(json_path, split_ext=True)[1].lower() == ".json", ".json required"

    import json

    with open(json_path, "r") as f_json:
        return json.load(f_json)
    

def load_jsonl(jsonl_path: Pathlike) -> Iterator[Any]:
    """
    Load a .jsonl file.

    Args:
        jsonl_path (Pathlike): Path to .jsonl

    Returns:
        Iterator[Any]: Loaded .jsonl
    """

    assert get_basename(jsonl_path, split_ext=True)[1].lower() == ".jsonl", ".jsonl required"

    import json

    with open(jsonl_path, "r") as f_jsonl:
        for line in f_jsonl:
            yield json.loads(line)


def load_yaml(yaml_path: Pathlike, safe: bool = True) -> Any:
    """
    Load a .yaml file.

    Args:
        yaml_path (Pathlike): Path to .yaml
        safe (bool, optional): Load `yaml_path` safely. Defaults to True.

    Returns:
        Any: Loaded .yaml
    """

    assert get_basename(yaml_path, split_ext=True)[1].lower() == ".yaml", ".yaml required"

    try:
        import yaml
    except ImportError:
        raise ImportError("Could not import yaml. Try `pip install -U pyyaml`.")
    
    with open(yaml_path, "r") as f_yaml:
        return yaml.safe_load(f_yaml) if safe else yaml.load(f_yaml)
    

def load_ini(ini_path: Pathlike) -> Any:
    """
    Load a .ini file.

    Args:
        ini_path (Pathlike): Path to .ini

    Returns:
        ConfigParser: Loaded .ini
    """

    def _load_ini(ini_path: Pathlike) -> ConfigParser:
        config = ConfigParser()
        config.read(ini_path)

        return config
    
    assert get_basename(ini_path, split_ext=True)[1].lower() == ".ini", ".ini required"

    from configparser import ConfigParser

    return _load_ini(ini_path)


def load_xml(xml_path: Pathlike) -> Any:
    """
    Load a .xml file.

    Args:
        xml_path (Pathlike): Path to .xml

    Returns:
        BeautifulSoup: Loaded .xml
    """

    def _load_xml(xml_path: Pathlike) -> BeautifulSoup:
        with open(xml_path, "r") as f_xml:
            return BeautifulSoup(f_xml.read(), features="html.parser")
        
    assert get_basename(xml_path, split_ext=True)[1].lower() == ".xml", ".xml required"

    from bs4 import BeautifulSoup

    return _load_xml(xml_path)
