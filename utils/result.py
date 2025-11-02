from typing import Generic, TypeVar, Union

from pydantic import validate_call

T = TypeVar("T")
E = TypeVar("E")


class ResultError(RuntimeError):
    pass


class Result(Generic[T, E]):
    @validate_call
    def __init__(self, is_ok: bool, value: Union[T, E]) -> None:
        self._is_ok = is_ok
        self._value = value

    def __repr__(self) -> str:
        return f"Ok({self.value})" if self.is_ok() else f"Err({self.value})"

    @classmethod
    def Ok(cls, value: T) -> "Result[T, E]":
        return cls(True, value)

    @classmethod
    def Err(cls, error: E) -> "Result[T, E]":
        return cls(False, error)

    def is_ok(self) -> bool:
        return self._is_ok

    def is_err(self) -> bool:
        return not self.is_ok()

    def unwrap(self) -> T:
        if self.is_ok():
            return self.value
        else:
            raise ResultError(f"Called unwrap() on Err: {self.value}")

    def unwrap_err(self) -> E:
        if self.is_err():
            return self.value
        else:
            raise ResultError(f"Called unwrap_err() on Ok: {self.value}")

    @property
    def value(self) -> Union[T, E]:
        return self._value
