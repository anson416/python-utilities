# -*- coding: utf-8 -*-
# File: hardware.py

"""
System hardware information.
"""

__all__ = [
    "get_n_cpu",
    "get_total_mem",
    "get_n_gpu",
]


def get_n_cpu() -> int:
    """
    Get the number of CPU cores.

    Returns:
        int: Number of CPU cores.
    """

    import multiprocessing
    return multiprocessing.cpu_count()


def get_total_mem() -> int:
    """
    Get the total amount of system memory (bytes).

    Raises:
        ImportError: Raise if psutil could not be imported.

    Returns:
        int: Total amount of system memory (bytes).
    """

    try:
        import psutil
        return psutil.virtual_memory().total
    except ImportError:
        raise ImportError("Could not import psutil. Try `pip install -U psutil`.")


def get_n_gpu() -> int:
    """
    Get the number of GPUs.

    Returns:
        int: Number of GPUs.
    """

    from .package import has_package
    has_torch, has_tf = has_package("torch"), has_package("tensorflow")
    assert has_torch or has_tf, "Need either PyTorch or Tensorflow."

    # Use PyTorch first, and then Tensorflow
    if has_torch:
        import torch
        return torch.cuda.device_count()
    else:
        import tensorflow as tf
        return len(tf.config.list_physical_devices("GPU"))
