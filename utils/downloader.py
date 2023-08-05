# -*- coding: utf-8 -*-
# File: downloader.py

import asyncio
import os
from typing import Optional, Union

try:
    import aiohttp
except ImportError:
    raise ImportError("Could not import aiohttp. Try `pip3 install -U aiohttp`.")
try:
    from sortedcollections import OrderedSet
except ImportError:
    raise ImportError("Could not import sortedcollections. Try `pip3 install -U sortedcollections`.")
try:
    from tqdm import tqdm
except ImportError:
    raise ImportError("Could not import tqdm. Try `pip3 install -U tqdm`.")

from . import beartype
from .file_ops import create_dir, get_basename
from .types import Array, Pathlike, StrDict

__all__ = ["download_files"]


class _URL(object):
    @beartype
    def __init__(
        self,
        url: Pathlike,
        file_name: Optional[str] = None,
    ) -> None:
        url = url.strip()
        if isinstance(file_name, str):
            file_name = file_name.strip()
        
        assert url, "URL cannot be empty"
        
        self._url = url
        self._file_name = file_name or get_basename(self._url)

    @property
    @beartype
    def url(self) -> Pathlike:
        return self._url
    
    @property
    @beartype
    def file_name(self) -> str:
        return self._file_name


@beartype
async def _download_file(
    url: Pathlike,
    file_path: Pathlike,
    session: aiohttp.ClientSession,
    sem: asyncio.Semaphore,
    all_bar: tqdm,
    leave: bool,
) -> tuple[Pathlike, Pathlike, Union[Exception, int]]:
    @beartype
    async def _download(
        url: Pathlike,
        file_path: Pathlike,
        session: aiohttp.ClientSession,
        leave: bool,
    ) -> int:
        async with session.get(url) as response:
            assert response.status == 200, f"Could not access {url}"
            
            size = int(response.headers.get("Content-Length", 0))
            ind_bar = tqdm(
                total=size, unit="B", unit_scale=True, unit_divisor=1024, miniters=1, mininterval=0.1, leave=leave,
                desc=file_path)
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

@beartype
def download_files(
    urls: Array[Union[Array[Pathlike], Pathlike]],
    download_dir: Pathlike = "./",
    replace_existing: bool = True,
    max_workers: int = 2,
    leave: bool = False,
    desc: Optional[str] = "Downloading files",
) -> StrDict[list[tuple[Pathlike, Pathlike, Union[Exception, int]]]]:
    @beartype
    async def _download_files(
        urls: list[tuple[Pathlike, Pathlike]],
        sem: asyncio.Semaphore,
        all_bar: tqdm,
        leave: bool,
    ) -> StrDict[list[tuple[Pathlike, Pathlike, Union[Exception, int]]]]:
        async with aiohttp.ClientSession() as session:
            tasks = [_download_file(*url, session, sem, all_bar, leave) for url in urls]
            results = {"succeeded": [], "failed": []}
            for result in await asyncio.gather(*tasks):
                results["succeeded"].append(result) if isinstance(result[-1], int) else results["failed"].append(result)
            
            return results
    
    download_dir = download_dir.strip()
    
    assert urls, "urls cannot be empty"
    assert download_dir, "download_dir cannot be empty"
    assert max_workers > 0, "max_workers must be positive integer"

    create_dir(download_dir)

    _urls = []
    for url in urls:
        if isinstance(url, str):
            url = (url,)
        url = _URL(*url)
        file_path = os.path.join(download_dir, url.file_name)
        if replace_existing or not os.path.exists(file_path):
            _urls.append((url.url, file_path))

    sem = asyncio.BoundedSemaphore(max_workers)

    with tqdm(total=len(_urls), desc=desc) as all_bar:
        loop = asyncio.get_event_loop()
        try:
            return loop.run_until_complete(_download_files(list(OrderedSet(_urls)), sem, all_bar, leave))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
