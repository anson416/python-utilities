# -*- coding: utf-8 -*-
# File: utils.py

from .types import Union

__all__ = [
    "has_package",
    "hashing",
]


def has_package(
    package_name: str,
    raise_err: bool = False,
) -> bool:
    """
    Return True if a package is installed in the current environment.

    Args:
        package_name (str): Name of package
        raise_err (bool, optional): Raise ImportError if `package_name` is not found

    Raises:
        ImportError: Raise if `raise_err` is True and `package_name` is not found

    Returns:
        bool: True if package_name is found
    """

    import importlib.util

    if importlib.util.find_spec(package_name):
        return True
    else:
        if raise_err:
            raise ImportError(f"Package \"{package_name}\" not found")
        else:
            return False


def hashing(
    msg: Union[str, bytes],
    algo: str = "sha",
    ver: int = 3,
    digest_size: int = 256,
) -> str:
    """
    Hash a message.

    Args:
        msg (Union[str, bytes]): Target message
        algo (str, optional): Algorithm used to hash. Must be any one in {"sha", "md5"}. Defaults to "sha".
        ver (int, optional): Specify the version of SHA hashing algorithm. Used only when `algo` is "sha". Must be any \
            one in {1, 2, 3}. Defaults to 3.
        digest_size (int, optional): Specify the digest size in SHA hashing algorithm. Used only when `algo` is "sha" \
            and `ver` in {2, 3}. Must be any one in {224, 256, 384, 512}. Defaults to 256.

    Raises:
        ValueError: Invalid `algo`
        ValueError: Invalid `ver`
        ValueError: Invalid `digest_size`

    Returns:
        str: Hashed message
    """

    import hashlib

    ALGO_DICT = {
        "sha": {
            1: hashlib.sha1,
            2: {
                224: hashlib.sha224,
                256: hashlib.sha256,
                384: hashlib.sha384,
                512: hashlib.sha512,
            },
            3: {
                224: hashlib.sha3_224,
                256: hashlib.sha3_256,
                384: hashlib.sha3_384,
                512: hashlib.sha3_512,
            },
        },
        "md5": hashlib.md5,
    }

    msg = msg.encode() if isinstance(msg, str) else msg
    
    if algo not in ALGO_DICT:
        raise ValueError(f"algo must be any one in {set(ALGO_DICT.keys())}")
    hash_algo = ALGO_DICT[algo]
    if isinstance(hash_algo, dict):
        if ver not in hash_algo:
            raise ValueError(f"ver must be any one in {set(hash_algo.keys())}")
        hash_algo = hash_algo[ver]
        if isinstance(hash_algo, dict):
            if digest_size not in hash_algo:
                raise ValueError(f"digest_size must be any one in {set(hash_algo.keys())}")
            hash_algo = hash_algo[digest_size]

    return hash_algo(msg).hexdigest()
    
    
