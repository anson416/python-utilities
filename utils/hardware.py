# -*- coding: utf-8 -*-
# File: hardware.py

import multiprocessing

from . import beartype
from .utils import has_package

__all__ = ["get_n_cpu",
           "get_total_mem",
           "get_n_gpu"]


@beartype
def get_n_cpu() -> int:
    """
    Get the number of CPU cores.

    Returns:
        int: Number of CPU cores
    """

    return multiprocessing.cpu_count()


@beartype
def get_total_mem() -> int:
    """
    Get the total amount of system memory.

    Raises:
        ImportError: Raise if psutil cannot be imported

    Returns:
        int: Total amount of system memory
    """

    try:
        import psutil
    except ImportError:
        raise ImportError("Cannot import psutil. Try `pip install -U psutil`.")
    
    return psutil.virtual_memory().total


@beartype
def get_n_gpu() -> int:
    """
    Get the number of GPUs.

    Returns:
        int: Number of GPUs.
    """

    has_torch, has_tf = has_package("torch"), has_package("tensorflow")

    assert has_torch or has_tf, "Need either pytorch or tensorflow"
    
    if has_torch:
        import torch
        n_gpu = torch.cuda.device_count()
    else:
        import tensorflow as tf
        n_gpu = len(tf.config.list_physical_devices("GPU"))
    
    return n_gpu