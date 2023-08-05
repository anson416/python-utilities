# -*- coding: utf-8 -*-
# File: config.py

from typing import Any

from . import beartype
from .file_ops import get_basename
from .types import Pathlike


@beartype
def load_json(json_path: Pathlike) -> Any:
    assert get_basename(json_path, split_ext=True)[1].lower() == ".json", ".json required"

    import json

    with open(json_path, "r") as f_json:
        return json.load(f_json)
    

@beartype
def load_jsonl(jsonl_path: Pathlike) -> list[Any]:
    assert get_basename(jsonl_path, split_ext=True)[1].lower() == ".jsonl", ".jsonl required"

    import json

    with open(jsonl_path, "r") as f_jsonl:
        return [json.loads(line) for line in f_jsonl]


@beartype
def load_yaml(yaml_path: Pathlike, safe: bool = True) -> Any:
    assert get_basename(yaml_path, split_ext=True)[1].lower() == ".yaml", ".yaml required"

    try:
        import yaml
    except ImportError:
        raise ImportError("Could not import yaml. Try `pip3 install -U pyyaml`.")
    
    with open(yaml_path, "r") as f_yaml:
        return yaml.safe_load(f_yaml) if safe else yaml.load(f_yaml)
    

@beartype
def load_ini(ini_path: Pathlike) -> Any:
    @beartype
    def _load_ini(ini_path: Pathlike) -> ConfigParser:
        config = ConfigParser()
        config.read(ini_path)

        return config
    
    assert get_basename(ini_path, split_ext=True)[1].lower() == ".ini", ".ini required"

    from configparser import ConfigParser

    return _load_ini(ini_path)


@beartype
def load_xml(xml_path: Pathlike) -> Any:
    @beartype
    def _load_xml(xml_path: Pathlike) -> BeautifulSoup:
        with open(xml_path, "r") as f_xml:
            return BeautifulSoup(f_xml.read(), features="html.parser")
        
    assert get_basename(xml_path, split_ext=True)[1].lower() == ".xml", ".xml required"

    from bs4 import BeautifulSoup

    return _load_xml(xml_path)
