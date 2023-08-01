# -*- coding: utf-8 -*-
# File: hardware.py

import multiprocessing

from . import beartype
from .error import err2str, raise_err
from .logger import logger
from .utils import is_package_installed

__all__ = ["get_n_cpu",
           "get_total_mem",
           "get_n_gpu"]


@beartype
def get_n_cpu() -> int:
    """
    Return the number of CPU cores.

    Returns:
        int: Number of CPU cores
    """

    return multiprocessing.cpu_count()


@beartype
def get_total_mem() -> int:
    """
    Return the total amount of system memory.

    Returns:
        int: Total amount of system memory
    """

    try:
        import psutil
    except ImportError as e:
        err_msg = f"Cannot import psutil. Try `pip install -U psutil`. ({err2str(e)})"
        logger.error(err_msg)
        raise_err(e, msg=err_msg)
        
    return psutil.virtual_memory().total


@beartype
def get_n_gpu() -> int:
    """
    Return the number of GPUs.

    Returns:
        int: Number of GPUs.
    """
    
    if is_package_installed("torch"):
        import torch
        n_gpu = torch.cuda.device_count()
    elif is_package_installed("tensorflow"):
        import tensorflow as tf
        n_gpu = len(tf.config.list_physical_devices("GPU"))
    else:
        err_msg = "Need either pytorch or tensorflow"
        logger.error(err_msg)
        raise ImportError(err_msg)
    
    return n_gpu
