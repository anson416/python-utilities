from typing import Optional

from pydantic import validate_call


@validate_call
def get_datetime(format: str = r"%Y%m%d-%H%M%S") -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime(format)


@validate_call
def bytes_to_base64(b: bytes) -> str:
    import base64

    return base64.b64encode(b).decode("utf-8")


@validate_call
def base64_to_bytes(s: str) -> bytes:
    import base64

    return base64.b64decode(s)


@validate_call
def format_error(error: BaseException) -> tuple[str, str]:
    import traceback

    return (
        f"{error.__class__.__module__}.{error.__class__.__name__}: {str(error)}",
        traceback.format_exc(),
    )


@validate_call
def tsprint(
    *values: object, sep: Optional[str] = " ", end: Optional[str] = "\n"
) -> None:
    import sys

    from tqdm import tqdm

    with tqdm.external_write_mode(nolock=False):
        sys.stdout.write(sep.join(map(str, values)))
        sys.stdout.write(end)
        sys.stdout.flush()
