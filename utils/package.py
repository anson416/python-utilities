# -*- coding: utf-8 -*-
# File: utils/package.py

__all__ = [
    "has_package",
]


def has_package(
    package_name: str,
    raise_err: bool = False,
) -> bool:
    """
    Return True if a package is installed in the current environment.

    Args:
        package_name (str): Name of package.
        raise_err (bool, optional): Raise ImportError if `package_name` is not
            found.

    Raises:
        ImportError: Raise if `raise_err` is True and `package_name` is not
            found.

    Returns:
        bool: True if package_name is found.
    """

    import importlib.util

    if importlib.util.find_spec(package_name):
        return True
    else:
        if raise_err:
            raise ImportError(f'Package "{package_name}" not found')
        else:
            return False
