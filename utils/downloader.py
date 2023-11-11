# -*- coding: utf-8 -*-
# File: downloader.py

import asyncio
import os
from pathlib import Path
from typing import List, Optional, Tuple, Union

try:
    import aiohttp
except ImportError:
    raise ImportError("Could not import aiohttp. Try `pip install -U aiohttp`.")
try:
    from sortedcollections import OrderedSet
except ImportError:
    raise ImportError("Could not import sortedcollections. Try `pip install -U sortedcollections`.")
try:
    from tqdm import tqdm
except ImportError:
    raise ImportError("Could not import tqdm. Try `pip install -U tqdm`.")

from .file_ops import create_dir, get_basename
from .formatter import trunc_str
from .types_ import Array, PathLike, StrDict

__all__ = ["download_files"]


async def _download_file(
    url: PathLike,
    file_path: PathLike,
    session: aiohttp.ClientSession,
    sem: asyncio.Semaphore,
    all_bar: tqdm,
    leave: bool = False,
) -> Tuple[PathLike, PathLike, Union[int, Exception]]:
    async def _download(
        url: PathLike,
        file_path: PathLike,
        session: aiohttp.ClientSession,
        leave: bool = False,
    ) -> int:
        async with session.get(url) as response:
            assert response.status == 200, f"Could not access {url}"
            
            size = int(response.headers.get("Content-Length", 0))
            ind_bar = tqdm(
                total=size, unit="B", unit_scale=True, unit_divisor=1024, miniters=1, mininterval=0.1, leave=leave,
                desc=trunc_str(file_path, 50, mode=4, replacement="..."))
            with open(file_path, mode="wb") as f, ind_bar:
                async for chunk in response.content.iter_chunked(512):
                    f.write(chunk)
                    ind_bar.update(len(chunk))

        return size

    try:
        async with sem:
            size = await _download(url, file_path, session, leave)
    except Exception as e:
        return url, file_path, e
    finally:
        all_bar.update()

    return url, file_path, size

def download_files(
    urls: Array[Union[Array[Union[PathLike, str]], PathLike]],
    download_dir: PathLike = "./",
    replace_existing: bool = True,
    max_workers: int = 2,
    leave: bool = False,
    desc: Optional[str] = "Downloading files",
) -> StrDict[List[Tuple[PathLike, PathLike, Union[int, Exception]]]]:
    """
    Download multiple files from the Internet concurrently.

    Args:
        urls (Array[Union[Array[Union[PathLike, str]], PathLike]]): URLs of files to be downloaded. Must be an Array \
            (list or tuple), in which each element is either a URL or an Array in which the first element is a URL and \
            the second element is a file name.
        download_dir (PathLike, optional): Directory to which files will be downloaded. Defaults to "./".
        replace_existing (bool, optional): Download existing files again. Defaults to True.
        max_workers (int, optional): Max. number of files that can be downloaded at the same time. Defaults to 2.
        leave (bool, optional): Keep progress bar for each file. Defaults to False.
        desc (Optional[str], optional): Description for the overall progress bar. Defaults to "Downloading files".

    Returns:
        StrDict[List[Tuple[PathLike, PathLike, Union[int, Exception]]]]: A dictionary in the form \
            {"succeeded": [], "failed": []}. Each 3-tuple in the list of "succeeded" contains URL, file name and file \
            size. Each 3-tuple in the list of "failed" contains URL, file name and raised exception.
    """

    async def _download_files(
        urls: List[Tuple[PathLike, PathLike]],
        sem: asyncio.Semaphore,
        all_bar: tqdm,
        leave: bool = False,
    ) -> StrDict[List[Tuple[PathLike, PathLike, Union[int, Exception]]]]:
        async with aiohttp.ClientSession() as session:
            tasks = [_download_file(*url, session, sem, all_bar, leave) for url in urls]
            results = {"succeeded": [], "failed": []}
            for result in await asyncio.gather(*tasks):
                results["succeeded"].append(result) if isinstance(result[-1], int) else results["failed"].append(result)
            
            return results
        
    def _process_url(
        url: PathLike,
        filename: Optional[str] = None
    ) -> Tuple[str, str]:
        url = str(url).strip()
        if isinstance(filename, str):
            filename = filename.strip()
        
        assert url != "", f"\"{url}\" is empty. URL must not be empty."

        return url, filename or get_basename(url)
    
    download_dir = download_dir.strip()
    
    assert urls != [], f"{urls} is empty. urls must not be empty."
    assert download_dir != "", f"\"{download_dir}\" is empty. download_dir must not be empty."
    assert max_workers > 0, f"{max_workers} <= 0. max_workers must be a positive integer"

    create_dir(download_dir)

    _urls = []
    for url in urls:
        if any(map(lambda x: isinstance(url, x), (str, Path))):
            url = (url,)
        url, filename = _process_url(*url)
        file_path = os.path.join(download_dir, filename)
        if replace_existing or not os.path.exists(file_path):
            _urls.append((url, file_path))

    sem = asyncio.BoundedSemaphore(max_workers)

    with tqdm(total=len(_urls), desc=desc) as all_bar:
        loop = asyncio.get_event_loop()
        try:
            return loop.run_until_complete(_download_files(list(OrderedSet(_urls)), sem, all_bar, leave))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
