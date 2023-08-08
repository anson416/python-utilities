#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: setup.py

from setuptools import setup, find_packages
NAME = 'utils'
DESCRIPTION = 'My short description for my project.'
URL = 'https://github.com/anson416/utilities'
EMAIL = 'lamyiufung2003@gmail.com'
AUTHOR = 'Awesome Soul'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = '0.1.0'

setup(
    name=NAME,
    version=VERSION,
    install_requires=[
        "aiohttp",
        "beartype",
        "beautifulsoup4",
        "colorama",
        "psutil",
        "sortedcollections",
        "termcolor",
        "tqdm",
        "pyyaml",
    ],
    packages=find_packages(),
)

# print(find_packages())

# setup(
#     name=NAME,
#     version=about['__version__'],
#     description=DESCRIPTION,
#     long_description=long_description,
#     long_description_content_type='text/markdown',
#     author=AUTHOR,
#     author_email=EMAIL,
#     python_requires=REQUIRES_PYTHON,
#     url=URL,
#     packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
#     # If your package is a single module, use this instead of 'packages':
#     # py_modules=['mypackage'],

#     # entry_points={
#     #     'console_scripts': ['mycli=mymodule:cli'],
#     # },
#     install_requires=REQUIRED,
#     extras_require=EXTRAS,
#     include_package_data=True,
#     license='MIT',
#     classifiers=[
#         # Trove classifiers
#         # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
#         'License :: OSI Approved :: MIT License',
#         'Programming Language :: Python',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.6',
#         'Programming Language :: Python :: Implementation :: CPython',
#         'Programming Language :: Python :: Implementation :: PyPy'
#     ],
#     # $ setup.py publish support.
#     cmdclass={
#         'upload': UploadCommand,
#     },
# )
