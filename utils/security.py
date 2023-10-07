# -*- coding: utf-8 -*-
# File: security.py

from .types import Optional, Union

__all__ = [
    "hash_",
    "gen_key",
]


def hash_(
    msg: Union[str, bytes],
    algo: str = "sha",
    ver: int = 3,
    digest_size: int = 256,
    max_len: Optional[int] = None,
) -> str:
    """
    Hash a message.

    Args:
        msg (Union[str, bytes]): Target message
        algo (str, optional): Algorithm used to hash. Must be any one in {"sha", "md5"}. Note that MD5 hash algorithm \
            is NOT secure. Defaults to "sha".
        ver (int, optional): Specify the version of SHA hash algorithm. Used only when `algo` is "sha". Must be any \
            one in {1, 2, 3}. Defaults to 3.
        digest_size (int, optional): Specify the digest size in SHA hash algorithm. Used only when `algo` is "sha" \
            and `ver` is in {2, 3}. Must be any one in {224, 256, 384, 512}. Defaults to 256.
        max_len (Optional[int], optional): If not None, hashed message will be truncated to `max_len` characters. \
            Defaults to None.

    Raises:
        ValueError: Invalid `algo`. Must be any one in {"sha", "md5"}.
        ValueError: Invalid `ver`. Must be any one in {1, 2, 3}.
        ValueError: Invalid `digest_size`. Must be any one in {224, 256, 384, 512}.

    Returns:
        str: Hashed message
    """

    if max_len:
        assert max_len >= 0, "max_len must be non-negative integer"

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
    algo = algo.lower()
    
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

    return hash_algo(msg).hexdigest()[:max_len]


def gen_key(size: int = 32) -> bytes:
    """
    Generate random encoded string, which can be used in cryptography.

    Args:
        size (int, optional): Size of generated string (in bytes). Defaults to 32.

    Returns:
        bytes: Generated string
    """

    import base64
    import os

    return base64.urlsafe_b64encode(os.urandom(size))
