# -*- coding: utf-8 -*-
# File: security.py

from typing import Optional, Union, Literal

__all__ = [
    "hash_",
    "gen_key",
]


def hash_(
    msg: Union[str, bytes],
    algo: Literal["sha", "md5"] = "sha",
    ver: Literal[1, 2, 3] = 3,
    digest_size: Literal[224, 256, 384, 512] = 256,
    max_len: Optional[int] = None,
) -> str:
    """
    Hash a message.

    Args:
        msg (Union[str, bytes]): Target message.
        algo (str, optional): Algorithm used to hash. Must be any one in 
            {"sha", "md5"}. Note that MD5 hash algorithm is NOT secure. 
            Defaults to "sha".
        ver (int, optional): Specify the version of SHA hash algorithm. Used 
            only when `algo` is "sha". Must be any one in {1, 2, 3}. Defaults 
            to 3.
        digest_size (int, optional): Specify the digest size in SHA hash 
            algorithm. Used only when `algo` is "sha" and `ver` is in {2, 3}. 
            Must be any one in {224, 256, 384, 512}. Defaults to 256.
        max_len (Optional[int], optional): If not None, hashed message will be 
            truncated to `max_len` characters. Defaults to None.

    Raises:
        ValueError: Invalid `algo`. Must be any one in {"sha", "md5"}.
        ValueError: Invalid `ver`. Must be any one in {1, 2, 3}.
        ValueError: Invalid `digest_size`. Must be any one in 
            {224, 256, 384, 512}.

    Returns:
        str: Hashed message.
    """

    if max_len is not None:
        assert max_len >= 0, f"{max_len} < 0. max_len must be a non-negative integer."

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

    if (algo := algo.lower()) not in (algo_set := set(ALGO_DICT.keys())):
        raise ValueError(f"{algo} does not belong to {algo_set}. `algo` must be any one in {algo_set}.")
    if isinstance(hash_algo := ALGO_DICT[algo], dict):  # Chosen algorithm is SHA
        if ver not in (ver_set := set(hash_algo.keys())):
            raise ValueError(f"{ver} does not belong to {ver_set}. `ver` must be any one in {ver_set}.")
        if isinstance(hash_algo := hash_algo[ver], dict):  # Chosen version is either 2 or 3
            if digest_size not in (digest_set := set(hash_algo.keys())):
                raise ValueError(f"{digest_size} does not belong to {digest_set}. `digest_size` must be any one in {digest_set}.")
            hash_algo = hash_algo[digest_size]
    return hash_algo(msg.encode() if isinstance(msg, str) else msg).hexdigest()[:max_len]


def gen_key(size: int = 32) -> bytes:
    """
    Generate random encoded string, which can be used in cryptography.

    Args:
        size (int, optional): Size of generated string (in bytes). Defaults to 
            32.

    Returns:
        bytes: Generated string
    """

    import base64
    import os
    return base64.urlsafe_b64encode(os.urandom(size))
