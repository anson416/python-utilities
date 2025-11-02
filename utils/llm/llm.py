import logging
import random
import time
from copy import deepcopy
from datetime import datetime, timezone
from typing import (
    Annotated,
    Any,
    Generic,
    Literal,
    Optional,
    Sequence,
    TypeVar,
    Union,
)
from uuid import uuid4

from openai import InternalServerError, OpenAI, RateLimitError
from openai.types.chat import ChatCompletionTokenLogprob
from pydantic import BaseModel, Field, HttpUrl, validate_call

from ..dtypes import NonEmptyStr
from ..misc import format_error
from .dtypes import ImgLike
from .msg import Messages
from .response import ResponseModel, ResponseModelParsingError
from .template import PromptTemplate

DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."

ResponseType = TypeVar("ResponseType", bound=Union[ResponseModel, str])

logging.getLogger("httpx").setLevel(logging.WARNING)


class ChatParameters(BaseModel, validate_assignment=True, strict=True):
    model: NonEmptyStr
    max_tokens: Optional[Annotated[int, Field(ge=1)]] = None
    timeout: Optional[Annotated[float, Field(gt=0.0)]] = None
    max_retries: Optional[Annotated[int, Field(ge=0)]] = None
    base_url: Optional[HttpUrl] = None
    temperature: Optional[Annotated[float, Field(ge=0.0, le=2.0)]] = None
    image_detail: Optional[Literal["auto", "low", "high"]] = None
    reasoning_effort: Optional[Literal["low", "medium", "high"]] = None
    logprobs: Optional[bool] = None
    top_logprobs: Optional[Annotated[int, Field(ge=0, le=5)]] = None
    extra_body: Optional[dict[str, Any]] = None

    def to_api_params(self) -> dict[str, Any]:
        return self.model_dump(
            exclude={"timeout", "max_retries", "base_url", "image_detail"},
            exclude_none=True,
        )


class LlmOutput(
    BaseModel, Generic[ResponseType], validate_assignment=True, strict=True
):
    id: NonEmptyStr = Field(default_factory=lambda: uuid4().hex, frozen=True)
    created_at: NonEmptyStr = Field(
        default_factory=lambda: datetime.now(timezone.utc).strftime(
            r"%Y/%m/%d %H:%M:%S"
        ),
        frozen=True,
    )
    parameters: ChatParameters
    response: Optional[ResponseType] = None
    detail: Optional[NonEmptyStr] = None
    duration: Optional[Annotated[float, Field(gt=0.0)]] = None
    finish_reason: Optional[NonEmptyStr] = None
    prompt_tokens: Optional[Annotated[int, Field(ge=0)]] = None
    completion_tokens: Optional[Annotated[int, Field(ge=0)]] = None
    logprobs: Optional[list[ChatCompletionTokenLogprob]] = None
    messages: Optional[Messages] = None


class LlmChatError(RuntimeError):
    pass


class Llm(object):
    @validate_call
    def __init__(
        self,
        model: NonEmptyStr,
        max_tokens: Annotated[int, Field(ge=1)] = 4096,
        timeout: Annotated[float, Field(gt=0.0)] = 1800.0,
        max_retries: Annotated[int, Field(ge=0)] = 5,
        api_key: Optional[NonEmptyStr] = None,
        base_url: Optional[NonEmptyStr] = None,
    ) -> None:
        self._model = model
        self._max_tokens = max_tokens
        self._timeout = timeout
        self._max_retries = max_retries
        self._base_url = base_url
        self._client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self._messages = Messages()
        self._history: list[LlmOutput] = []

    @validate_call(config=dict(arbitrary_types_allowed=True))
    def __call__(
        self,
        prompt: Union[NonEmptyStr, PromptTemplate],
        response_type: type[ResponseType] = str,
        *,
        sys_prompt: Optional[NonEmptyStr] = DEFAULT_SYSTEM_PROMPT,
        temperature: Optional[Annotated[float, Field(ge=0.0, le=2.0)]] = None,
        images: Optional[Sequence[ImgLike]] = None,
        image_detail: Literal["auto", "low", "high"] = "auto",
        reasoning_effort: Optional[Literal["low", "medium", "high"]] = None,
        logprobs: Optional[bool] = None,
        top_logprobs: Optional[Annotated[int, Field(ge=0, le=5)]] = None,
        extra_body: Optional[dict[str, Any]] = None,
        base_delay: Annotated[float, Field(ge=1.0)] = 1.5,
    ) -> LlmOutput[ResponseType]:
        chat_parameters = ChatParameters(
            model=self._model,
            max_tokens=self._max_tokens,
            timeout=self._timeout,
            max_retries=self._max_retries,
            base_url=self._base_url,
            temperature=temperature,
            image_detail=image_detail,
            reasoning_effort=reasoning_effort,
            logprobs=logprobs,
            top_logprobs=top_logprobs,
            extra_body=extra_body,
        )

        # Dynamic system prompt
        if sys_prompt is not None:
            self._messages.add_system(sys_prompt)
        else:
            self._messages.remove_system()

        if len(self._messages) == 0 and sys_prompt is not None:
            self._messages.add_system(sys_prompt)
        self._messages.add_user(
            prompt() if isinstance(prompt, PromptTemplate) else prompt,
            images=images,
            image_detail=image_detail,
        )
        for r in range(self._max_retries + 1):
            start_time = time.perf_counter()
            llm_output = LlmOutput[ResponseType](parameters=chat_parameters)
            self._history.append(llm_output)
            delay = 0.0
            try:
                completion = self._client.chat.completions.create(
                    messages=self._messages.to_api_format(),
                    stream=False,
                    **chat_parameters.to_api_params(),
                )
                if len(completion.choices) == 0:
                    raise LlmChatError("LLM returned 0 choice")
                choice = completion.choices[0]
                asst_msg = choice.message.content
                if asst_msg is None:
                    raise LlmChatError("LLM response is None")
                response = (
                    response_type.from_str(asst_msg)
                    if issubclass(response_type, ResponseModel)
                    else asst_msg
                )
                if logprobs and choice.logprobs.content is None:
                    raise LlmChatError("LLM logprobs is None")
            except (
                InternalServerError,
                LlmChatError,
                RateLimitError,
                ResponseModelParsingError,
            ) as e:
                llm_output.detail = format_error(e)[0]
                if r == self._max_retries:
                    self._messages.remove_last()
                    raise
                delay = base_delay**r + random.random()
                time.sleep(delay)
                continue
            except Exception as e:
                llm_output.detail = format_error(e)[0]
                self._messages.remove_last()
                raise
            else:
                self._messages.add_assistant(asst_msg)
                llm_output.response = response
                llm_output.finish_reason = choice.finish_reason
                llm_output.prompt_tokens = completion.usage.prompt_tokens
                llm_output.completion_tokens = (
                    completion.usage.completion_tokens
                )
                llm_output.logprobs = (
                    choice.logprobs.content
                    if choice.logprobs is not None
                    else None
                )
                llm_output.messages = deepcopy(self._messages)
                break
            finally:
                llm_output.duration = time.perf_counter() - start_time - delay
        return self._history[-1]

    def clear_context(self) -> None:
        self._messages.clear()

    @property
    def history(self) -> list[LlmOutput]:
        return deepcopy(self._history)


def _cli() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str)
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("-t", "--temperature", type=float, default=None)
    parser.add_argument("--img", action="append", type=str, default=None)
    parser.add_argument("--api_key", type=str, default=None)
    parser.add_argument("--base_url", type=str, default=None)
    args = parser.parse_args()
    llm = Llm(args.model, api_key=args.api_key, base_url=args.base_url)
    llm_output = llm(
        args.prompt, temperature=args.temperature, images=args.img
    )
    print(llm_output.response)
