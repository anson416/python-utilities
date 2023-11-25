#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: setup.py

from pathlib import Path

from setuptools import find_packages, setup

NAME = "utils"
DESCRIPTION = "Utilities that can be used anywhere."
AUTHOR = "Anson Lam"
EMAIL = "lamyiufung2003@gmail.com"
PYTHON_VERSION = ">=3.8.0"
URL = "https://github.com/anson416/python-utilities"

with (Path(NAME) / "__init__.py").open() as f:
    version = [line.split("=")[-1].strip().strip("'\"")
               for line in f.read().splitlines() if line.startswith("__version__")][0]

with Path("./README.md").open() as f:
    long_description = f.read()

with Path("./requirements.txt").open() as f:
    install_requires = f.read().splitlines()

setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=PYTHON_VERSION,
    url=URL,
    packages=find_packages(),
    install_requires=install_requires,
    # license="Apache-2.0",
    classifiers=[  # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        # "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
    ],
)
