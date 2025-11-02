import mimetypes
from pathlib import Path
from typing import Annotated, Any, Literal, Optional, Sequence, Union

import cv2
import numpy as np
from PIL import Image
from pydantic import BaseModel, Field, validate_call

from ..dtypes import NonEmptyStr
from ..misc import bytes_to_base64
from .dtypes import ImgLike


@validate_call(config=dict(arbitrary_types_allowed=True))
def _encode_image(img: ImgLike) -> str:
    if isinstance(img, (Image.Image, np.ndarray)):
        if isinstance(img, Image.Image):
            img = np.array(img.convert("RGB"))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
            if not (len(img.shape) == 3 and img.shape[-1] == 3):
                raise ValueError("ndarray must be (H, W, 3)")
        mime = "image/jpeg"
        content = bytes_to_base64(cv2.imencode(".jpg", img)[1])
    elif isinstance(img, (Path, str)):
        if str(img).startswith(("http://", "https://")):
            return str(img)
        mime, _ = mimetypes.guess_type(img)
        if mime is None or not mime.startswith("image/"):
            mime = "application/octet-stream"
        with open(img, "rb") as f:
            content = bytes_to_base64(f.read())
    else:
        raise TypeError(f"Unsupported image type '{type(img)}'")
    return f"data:{mime};base64,{content}"


class Message(BaseModel, validate_assignment=True, strict=True):
    role: Literal["system", "user", "assistant"]
    content: Union[NonEmptyStr, list[dict[str, Any]]]


class Messages(BaseModel, validate_assignment=True, strict=True):
    messages: Annotated[list[Message], Field(default_factory=list)]

    def __len__(self) -> int:
        return len(self.messages)

    @validate_call
    def add_system(self, prompt: NonEmptyStr) -> None:
        msg = Message(role="system", content=prompt)
        if self.__len__() == 0:
            self.messages.append(msg)
        else:
            if self.messages[0].role == "system":
                self.messages[0].content = prompt
            else:
                self.messages.insert(0, msg)

    @validate_call(config=dict(arbitrary_types_allowed=True))
    def add_user(
        self,
        prompt: NonEmptyStr,
        images: Optional[Sequence[ImgLike]] = None,
        image_detail: Literal["auto", "low", "high"] = "auto",
    ) -> None:
        content = [{"type": "text", "text": prompt}]
        if images is not None:
            for img in images:
                content.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": _encode_image(img),
                            "detail": image_detail,
                        },
                    }
                )
        self.messages.append(Message(role="user", content=content))

    @validate_call
    def add_assistant(self, response: str) -> None:
        self.messages.append(Message(role="assistant", content=response))

    def clear(self) -> None:
        self.messages.clear()

    def remove_last(self) -> None:
        if self.__len__() > 0:
            self.messages.pop()

    def remove_system(self) -> None:
        if self.__len__() > 0 and self.messages[0].role == "system":
            self.messages.pop(0)

    def to_api_format(self) -> list[dict[str, Any]]:
        return [msg.model_dump() for msg in self.messages]
